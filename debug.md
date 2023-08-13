# Debugging the worst-case scenario: it's not your fault; & Windows-devs matter! ✊

## TLDR;

I am using windows for other vital reasons(not gaming). I wanted to embed a rust crate which is supposedly cross-platform. But since windows development is overlooked, it was not easy as it sounds. Here's my write-up on debugging the hell out of a fairly large codebase. This is one of the worst-case scenarios where the <mark>problem is not you, but the dependency of the dependency that you depend on</mark>. Watch me hop rust to C then to GNU Posix utils and back to Windows.

---

## <mark>Disclaimer</mark>

I am NOT nit-picking on [*surrealdb*](https://surrealdb.com) community. This is just an example. The maintainers pull the PR right away like they were waiting on someone to do this. The *surrealdb* community is the first most active community I have seen so far other than live O\*lyFa\*s 😅.

---

# The Problem Definition

I was working on a side project using Tauri back in Aug. 2022. For data persistence I decided on SQLite, then this video from [fireshipio](https://www.youtube.com/@Fireship).

%[https://www.youtube.com/watch?v=C7WFwgDRStM] 

**Just found What I needed!**

So, I went ahead and looked at the LICENCE, it permitted use *in* the app (but not as a separate service). I cloned it, and start migrating from SQLite to SurrealDB! Took me a couple of days to adopt but the codebase was well documented so, ON PAPER everything was sound! Execute `cargo tauri dev` 🚀

🤦‍♂️ Should have used [rust-analyzer](https://rust-analyzer.github.io/).

My app no longer compiles. No this is not about rust being picky about borrows and such. It was something else ( spoiler: it's the dependency of a dependency )

---

# <mark>Disclaimer 2</mark>

<mark>This happened almost half a year ago, I can't replicate exactly what happened because a lot changed since then. You have to take my word here and there.</mark>

---

# The *NOW* problem

My build failed. So I started digging into my code, maybe it's me I guessed at first. I commented out new snippets of codes, and tried `println!` every single lexeme.

*I get it, but let's just say it, we teach and preach* `debug!(_)` *is the way to do it, but end up* `println("{:#?}", _)` *at the end of the day.*

**Nope!** my binary crate should compile for either `println!` and `debug!` to work. 🤦‍♂️

# The *rustc* to rescue 🦸‍♂️

One thing rust brings to take other than security and low-level control is the best compiler error messages. It even suggests what to do sometimes, but my fate it did not do a better job. But I vaguely remember it did 😅.

**<mark>GOLDEN RULE</mark> when your code doesn't compile: <mark>Patiently read the error message</mark>**

I had to learn this the **hard** way 😭. I didn't read well enough but just assumed it was me who messed up. In my defense, the *crate* `surrealdb` is of rust, cross-platform software and a binary was available from **choclately** by the first party! So, I presumed it is something I did.

I scorned through my codebase here and there, slapping `unwrap()` and `expect()` without a second thought, but nothing worked. I remember being soaked up into this, I ate dinner at 10-ish which should have been 6-ish 😖. I took a-sleep and woke up next early morning around 3 to, yeah, DEBUG 🧙‍♂️.

I tried all sorts of tricks, two being:

1. [lldb](https://lldb.llvm.org/): because at the end of the day, rustc converts `*.rs` into [`llvm`](https://www.infoworld.com/article/3247799/what-is-llvm-the-power-behind-swift-rust-clang-and-more.html)
    
2. [radare](https://rada.re/): individually compiled `rlibs`.
    

Why bizarre approach? Because I am coming from Reversing Background, these are what I have used so far. I didn't know how to debug properly back then. At last, I suspected the *macros.* So I examined the macro expanded rust files. Nope, I didn't see any faults as of my knowledge.

```bash
rustc -Zunpretty=expanded test.rs
```

Use this 👆 to see the expanded rust file.

---

# <mark>Bugs' implicit impact on health</mark>

If you have ever been debugging, you can feel what I am tryna say. It's not just your code that is broken, but you too! I could feel my body starts to take a step back. I felt like programming isn't for me. Computer Science is not my thing. I didn't sleep well. I was stressed and depressed. I no longer felt hungry. Furthermore, I was DISAPPOINTED in myself!

I couldn't even add a dependency and get my application to compile, how am I going to solve any *new* challenges?

I hope you can relate when the debugging took almost 2 days 🙆‍♂️. I took a deep breath and decided to take a break and come fresh.

---

# New Dawn

Instead of continuing, I decided to start fresh. You know that weird case, where restarting the computer fixes some issues! Same here. I executed

```bash
rm -rf ./out/ && \
cd src-tauri && cargo clean
```

Then tried to compile it again with

```bash
cargo tauri dev
```

It failed. Still not following the GOLDEN RULE, I decided to analyze the generated `pdb`. Then It hit me. I couldn't find neither *rlib* nor *pdb* for my binary crate. That's when I went back and read the **error** message.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676940169814/325335c0-8231-4cfa-97af-679e55160b28.png)

The compiler never got to my crate, it failed during the compilation of a dependency crate called `rquickjs`.

`LIBCLANG_PATH not found` is the essence. But, why the hell does a **rust** crate require a **C** compiler 🤷‍♂️. So I dug into the rabbit hole. The culprit is allegedly

```bash
C:\Users\b\.cargo\registry\src\github.com-1ecc6299db9ec823\bindgen-0.60.1\src/lib.rs:2172:31
```

Module's doc is

```rust
//! Generate Rust bindings for C and C++ libraries.
//!
//! Provide a C/C++ header file, receive Rust FFI code to call into C/C++
//! functions and use types defined in the header.
//!
//! See the [`Builder`](./struct.Builder.html) struct for usage.
//!
//! See the [Users Guide](https://rust-lang.github.io/rust-bindgen/) for
//! additional documentation.
```

So, **FFI I presume**. 🤦‍♂️. dependency `rqucikjs` uses `bindgen` to crate FFI to use some C library.

*Yes, there's a teeny-tiny chance surrealdb can* ***seg-fault*** *which this* [*video*](https://youtu.be/DPQbuW9dQ7w?t=20) *claims it can't implicitly.*

What C library? `libclang.dll`? I have the entire suite of *LLVM 13* on my machine. So I went ahead and peeped into `build.rs` for these bindings. The `main` being

```rust
fn main() {
    target::main();
    testgen::main();

    // On behalf of clang_sys, rebuild ourselves if important configuration
    // variables change, to ensure that bindings get rebuilt if the
    // underlying libclang changes.
    
    // buch of println snipped for brevity
}
```

`{target, testgen}::main()` 🤔wonder what they do.

```rust
// target::main
pub fn main() {
        let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());

        let mut dst =
            File::create(
                Path::new(&out_dir).join("host-target.txt")
            ).unwrap();
        dst.write_all(
                env::var("TARGET").unwrap().as_bytes()
            ).unwrap();
    }

// testgen::main
pub fn main() {
        // some snipped
        let headers = match fs::read_dir(headers_dir) {
            Ok(dir) => dir,
            // We may not have headers directory after packaging.
            Err(..) => return,
        };

        // --snip--
        for entry in entries {
            match entry.path().extension().and_then(OsStr::to_str) {
                Some("h") | Some("hpp") => {
                    let func = entry // ... --snip--
                    writeln(_) // --snip--
                }
                _ => {}
            }
        }

        dst.flush().unwrap();
    }
```

They seemed to create a file specific to **OS** and write some *tests* for generated headers. Nothing extraordinary, but did you notice some ENV\_VARs? Never have I ever set them. So someone up the tree **bootstraps** and **invokes**. Who is that?

### rquickjs

One niche feature of *surrealdb* is using JavaScript (ES2020, I guess) and WebAssembly to program *macro*s into database system (analogous to [pgSQL, pg/Tcl, pg/Python etc.](https://www.postgresql.org/docs/current/xplang.html))

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676942261044/bc3eae20-5a74-43f3-ad1f-74f5490e2b22.png)

The dependency is defined as:-

```ini
[dependencies.js]
# says optional, but couldn't find a way to compile without it
optional = true 
# --snip--
package = "rquickjs"
```

Few scroll up the error message

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676942773032/291e3a27-4edd-430f-99ab-5054d0e0d09a.png)

`rquickjs`'s *build.rs*

```rust
fn main() {
// --snip--
    let src_dir = Path::new("quickjs");
// --snip--
}
```

`rquickjs` is the port of `quickjs` to rust 🤦‍♂️. So, that's why I need **clang.** Let's get the **clang**. Installed it and added it to the PATH 💦. Let's go 🏃‍♀️.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676943674528/ec0d395b-2c84-4406-9e91-d40ef0b15968.png)

Note this ain't cargo, this is clang itself. And `stdio.h` not found? that's where even **Helloworld** in **C** starts 😲. Looking at *SearchPath ( aka InstallledDirs)...*

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676943848787/72a546f3-a677-48b6-bc49-53f4b8f62c5b.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676944046523/3d104d71-7595-4161-90b9-c0d6439179bb.png)

I didn't have *Visual Studio*, just the *build tools* but of 2022 😒. But how the heck is trivial `stdio.h` missed from *mingw64*? But, wait 🤚

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676944272257/d3a6ec97-5705-43c2-a6db-7c443dc87536.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676944381943/28ea4243-129c-48c5-a023-e9f2e415dbbe.png)

Are you kidding me right now? Wait, notice bare-clang is gcc (the prompt) but rust invoked-clang is msvc. Changing the target triple...

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676947374059/42108215-ade9-450b-8e4d-82253720eaf4.png)

Hooray 🥳 but changing the target triple is just a 🩹. Doing that with clang gives...

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676947472159/44f90fbf-97c1-412e-9f5e-af6320af566d.png)

the same error but with a suggestion to run from dev-cmd. Let's do that! I opened the developer cmd (Start &gt; type `dev cmd 64` &gt; this is it ✌).

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676956078324/3cb83acb-032f-44c0-b5de-bd3f0e19195c.png)

Hooray again 🥳. Why? Cause the error changed! That means we somehow fixed the previous one and we are nearby success 🎉🍾. What's this?

### Program Not Found

Seems like we need a binary and the error is still from `rquickjs`. This makes me wish *surrealdb*'s JS/WA *macro* is a **bane** than a **boon**. Nevertheless, let's read the message, and seems like line **136** causes the error.

```rust
fn patch<D: AsRef<Path>, P: AsRef<Path>>(out_dir: D, patch: P) {
    let mut child = Command::new("patch")
        .arg("-p1")
        .stdin(Stdio::piped())
        .current_dir(out_dir)
        .spawn() // 👈 line 136
        .expect("Unable to execute patch, you may need to install it: {}");
    println!("Appliyng patch {}", patch.as_ref().display());
    {
        let patch = fs::read(patch).expect("Unable to read patch");

        let stdin = child.stdin.as_mut().unwrap();
        stdin.write_all(&patch).expect("Unable to apply patch");
    }

    child.wait_with_output().expect("Unable to apply patch");
}
```

`spawn()`? Invoking an external binary. Even though `expect()` is to help, it seems like it is not very useful. Very strange 🤔. Aren't rust's `expect`s supposed to exit with that message if `panic` should happen? unpredictable behavior of *rustc*?

Makes me wonder whether rust holds up to the claims the community has been making. Here seems like `expect()` within `spawn()` fired before user-defined `expect` fired. Should `std::io` functions *propagate* the `Err` upstream instead of handling itself. **Please let me know in the comments why this happens.**

Back to the point. Seems like we are *patching!* Another layer unviels 🧅!

# The patches

GNU util, `patch` is used to apply *diffs* to files. If you have used [suckless](https://suckless.org/) programs you should be familiar with any other bdiffs. This is why my title says

### Windows-devs matter! ✊

Cross-platform is a bit of a lie in this case. Without a proper environment, *surrealdb* or any other crate depending on `rquickjs` can't be compiled. Because the GNU util `patch` isn't available by default. And at line 63-ish `rquickjs/build.rs` defines the *patch* files.

```rust
  let mut patch_files = vec![
        "check_stack_overflow.patch",
        "infinity_handling.patch",
        "atomic_new_class_id.patch",
    ];
```

Luckily GNU utils are being ported to native NT-kernel. These can be found [here](https://gnuwin32.sourceforge.net/packages/coreutils.htm). And we need this, [patch](https://gnuwin32.sourceforge.net/packages/patch.htm). So, I extracted it to a directory that is in my *System* PATH and run the *build* again. And 🥁 please...

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676958202626/01fc60f8-3cd1-49da-bb7f-5ad8e3e691c9.png)

Wooooooo🥳🎉🍾🥂🎇🎊🎓ooooowwwwww ! 😃 It took me weeks to figure this out back then. Now, I can proudly embed the crate and continue my project.

---

# So, What should be done?

1. Install Visual Studio Build Tools and Windows SDK (for `quickjs` from `rquickjs`)
    
2. Get `GNU pacth` (comes bundles with Git I now realize)
    
3. Run the build commands in `Developer Prompt` from Visual Studio
    

Like I told you, this is a <mark>WORST</mark> case scenario because conventional `println`, `debug`, *breakpoints* and `pdb`s wouldn't help us. Only the compiler and patient **Googling** will get you going.

---

# My first contribution to Open Source

Back then, I searched *surrealdb*'s **Discord** server for answers, but none. One time someone asked about it and decided to use WSL. I could have done that but I don't have memory enough to run WSL Vmmem and 422 rustc build commands. That is the first reason I couldn't afford to run *rust-analyzer* in the first place. So I decided to update the doc and have them merged for others to save time and hair they would be plucking otherwise.

[![https://github.com/surrealdb/surrealdb/pull/256/commits/85860497391dce1b67418576b1b6bf03485a1b26](https://cdn.hashnode.com/res/hashnode/image/upload/v1676959512081/f071c9b1-60df-42c7-82dd-8e4050ecb9d7.png)](https://github.com/surrealdb/surrealdb/pull/256/commits/85860497391dce1b67418576b1b6bf03485a1b26)

To my surprise, the merge was kinda instant. And that is how I earned my first **PullShark** badge in GitHub 🥇. The [PR](https://github.com/surrealdb/surrealdb/pull/256/commits/85860497391dce1b67418576b1b6bf03485a1b26).

---

# <mark>Few more disclaimers</mark>

For keen eyes, my PR suggests a different approach. That is because when I encountered the problem back then, it was how I managed to get it running. I tried replicating it for the #DebuggingFeb and end up finding a better yet less overhead way. I will make sure this alternative way is added to the docs via a new PR as well.

And, as of now (Feb 21, 2023) someone else sugar-coated the instructions and made it better than what I suggested, reducing PowerShell commands to invoke.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676959995039/c78f25b3-6f85-400e-8f40-fe608341aea0.png)

### But elevated? \[Bonus about Windows\]

Yes, you need to execute the commands in the elevated shell for the `patch` sys command to succeed. Why? Windows 😒. Windows implicitly assumes if a filename contains *setup/patch/installer* and *exe*, it requires Administrator rights to be invoked. Nothing serious. You can rename *patch* to whatever you want and can confirm it. But by then the build will fail, as it looks for *patch* itself.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676965334646/682b7a83-f18a-41c8-b487-2fdb7e5835c0.gif)

> **If you put the *patch* inside a privileged folder (e.g. ProgramFiles etc.) this *might not* be necessary.**

* I said *surrealdb* can SegFault, but it seems like taken a little bit of care, idk 🤷‍♂️ for sure though.
    

```c
 /* from: rquickjs/sys/patches/check_stack_overflow.patch */

diff --git a/quickjs.c b/quickjs.c
index 48aeffc..45077cb 100644
--- a/quickjs.c
+++ b/quickjs.c
@@ -1590,9 +1590,7 @@ static inline uintptr_t js_get_stack_pointer(void)
 static inline BOOL js_check_stack_overflow(JSRuntime *rt, size_t alloca_size)
 {
-    uintptr_t sp;
-    sp = js_get_stack_pointer() - alloca_size;
-    return unlikely(sp < rt->stack_limit);
+    return unlikely(js_get_stack_pointer() < rt->stack_limit + alloca_size);
 }
```

---

# My learning outcomes

1. Read the compiler error message first without assuming it's your new snippet that messes up 🔍
    
2. Don't just underestimate yourself but underestimate the dependencies as well 😎
    
3. Cross-Platform is not "cross" always ❌
    
4. Using Linux for development will keep your a\*\* out of pain most of the time. ⚰
    
5. Take a deep breath and Google it 🦸‍♂️
    

[![](https://cdn.hashnode.com/res/hashnode/image/upload/v1676965124276/b7a4768a-9d7e-49e9-b4db-cfed34b8e9b5.jpeg)](https://breakbrunch.com/software-developers-are-professional-google-searcher/)

---

# extra bits

1. [quickjs](https://bellard.org/quickjs/): lightweight javascript engine
    
2. [rquickjs](https://github.com/DelSkayn/rquickjs): high-level bindings of quickjs to rust FFI
    
3. [patch](https://gnuwin32.sourceforge.net/packages/patch.htm): utility used to apply the diff to a file
    
4. [LLVM](https://llvm.org/docs/LangRef.html): a suite of frontend and backend binaries for programming languages
    
5. [lldb](https://lldb.llvm.org/): a debugger from the LLVM suite
    
6. [radare2](https://rada.re/): a disassembler, patcher, differ, decompiler and all sorts of magical reversing utility
    
7. [Visual Studio Build tools](https://visualstudio.microsoft.com/downloads/?q=build+tools): Microsoft's softwares for compiling, linking etc. for Windows OS
    
8. [mingw](https://www.mingw-w64.org/): a set of tools from GNU Linux
    

# Epilogue

That's it. Seems like a hell of a long blog. But, took me weeks of depression and stress along with red fonts, LLVM docs, Windows SDK docs, and deeper research of Windows and Linux Differences to figure it out back in Sep 2022.

IDK whether this would be useful for someone else but I loved hopping from *rust* to *C* to *POSIX utils* and back to *rust. That was quite a journey back then.* And may this be an example of sometimes you need to go out of your comfy zone to get what you need.

**Till I see you in the next blog, this is** *me the BE* **👋, *signing off*.**

Cover background by Milad Fakurian.

---