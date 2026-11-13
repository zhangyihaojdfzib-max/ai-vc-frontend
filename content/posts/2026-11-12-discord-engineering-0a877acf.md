---
title: 'Discord <3 Linux: A Year of Upgrades'
title_original: 'Discord <3 Linux: A Year of Upgrades'
date: '2026-11-12'
source: Discord Engineering
source_url: https://discord.com/blog/discord-linux-a-year-of-upgrades
author: ''
summary: '[翻译失败，原文如下]


  # Discord <3 Linux: A Year of Upgrades


  Over the past year, we''ve been making Discord feel at home on Linux: a brand-new
  updater, faster ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:39.454586'
---

[翻译失败，原文如下]

# Discord <3 Linux: A Year of Upgrades

Over the past year, we've been making Discord feel at home on Linux: a brand-new updater, faster screen sharing, Wayland support across the board, and some love for the Steam Deck. Let's get into it!

## Updates That Just Update

If you're on Linux, you know how it goes: Discord says there's an update, you go download and install a fresh package, and you do it allagainnext week. We heard you.

The days of downloading a fresh .deb every week are over. Getting there meant working around some very Linux-y constraints. Distro packages install to places like /usr/bin that Discord can't write to without root, but packages aren't supposed to put files in your home folder either. Immutable distros like SteamOS and Bazzite lock down the base system and get most apps through Flatpak. Plenty of you install Discord from community packages built from our tarball (hi, AUR!). We needed something that worked for all of these formats. In the end, we settled on a new Rust-based updater that installs like a normal package, but installs the updates in a writable location.‍

![](/images/posts/a6199664fbe7.png)

The result is a big quality-of-life upgrade:

- Install once, update forever.The .deb, .rpm, Arch package, and tarball are now a small bootstrapper that installs Discord into your home directory. After that, Discord updates itself, no sudo required.
- Delta patches.Updates arrive as binary diffs (usingbsdiff), so you only download what changed. Files whose contents and permissions haven't changed are skipped entirely (updates were previously chunked only on a per-file basis).
- Faster updates.Decompression is now multithreaded, and each package installs as soon as its download finishes. We measured that delta updates on Linux are, on average, about 23% faster.
- More formats.The download page now offers .rpm and .pkg.tar.zst next to .deb and .tar.gz. Fedora and Arch folks, we see you.

This new updater required changes from the various Discord packages the community maintains, so big thanks to those maintainers for helping get this rolled out.

## Go Live with More Wayland and More Hardware

X11 and Wayland are the two main windowing systems on Linux, and they handle screen capture very differently. X11 is laissez-faire, while Wayland is built around isolation and privacy: apps can't see your screen or each other's windows unless you say so. Wayland is now the default on most major distros, so that's the future we built for. We teamed up withIgalia, experts in Linux screensharing, to build a great screenshare experience across different platforms and desktops.

Wayland exposes a screen or app sharing handle through a system dialog, so nothing is shared with the app until the user gives permission. Once granted, Discord receives access to a PipeWire stream that carries video frames of the selected screen or window. Discord submits the captured frames for hardware encoding throughVA-APIon supported Intel and AMD GPUs, orNVENCon supported Nvidia GPUs. The compressed bitstream is then returned to Discord, encrypted, and sent over the network to other clients.‍

![A sequence diagram of the Discord app subscribing to a Pipewire handle, receiving frames, and sending them to the encoder.](/images/posts/a4a6139abfd9.png)

Here's what changed:

- Wayland screenshare.We now leverage existing Wayland and PipeWire capabilities to lighten CPU load and make better use of your GPU. This is enabled for GNOME, KDE, gamescope, and other compositors.
- Steam Deck.Go Live works in both Game Mode (gamescope) and Desktop Mode, so you can stream efficiently on the go.
- Hardware encoding.We now support more OS- and GPU-supplied hardware video encoding formats. This makes sure that your NVIDIA, Intel, or AMD GPU is used to the max, while the CPU remains free for your game.

![](/images/posts/be026308994e.png)

## Push-to-Talketc.on Wayland

Global keybinds on Wayland were a long-standing pain point. Wayland (rightly) doesn't let apps listen to your keyboard in the background. Instead, it provides aGlobalShortcuts API, but the implementation can be a little tricky. The spec says a shortcut looks like "<Control>z", but KDE expects "CTRL+z", so Discord figures out which desktop you're on and speaks its dialect (send the wrong one and the portal session can fall over entirely). And since every bind request can pop up an approval dialog, we only ask again when your keybinds actually change, instead of nagging you every time Discord starts. Now, features like push-to-talk work on Linux, even when Discord isn't focused.

## What's Next: More Control of Sound Sharing

We’ve covered a lot of Linux improvements, but there’s more to do before we reach parity with the other desktop platforms. That means changing to the Wayland infrastructure itself. We use xdg-desktop-portal for screenshare, but that doesn’t provide a handle to capture app audio. Linux users have to choose between sharing audio for their whole desktop or sharing no audio at all. That’s not an experience we can accept long term, so we’re building per-app audio sharing on Wayland and giving it to the Linux community.

We’ve once again teamed up with Igalia to implement per-app audio sharing in xdg-desktop-portal, letting you pick exactly which app's audio is shared. We’re even implementing it on GNOME and KDE ourselves to get it to users faster. This will take some time to reach critical mass across Linux desktops, but it’s a long-term investment to make a great Linux screenshare experience for both Discord and all screensharing apps. Stay tuned!

## See You in the Call

Linux folks, this one's for you. Update Discord (well, let it update itself, finally), hop in a call, and hang out. And if building this stuff sounds fun,we're hiring.

*hands the penguin a headset and waves goodbye*🐧

![](/images/posts/018b95600984.png)

### Discord Patch Notes: November 9, 2026

### Unlock, Level Up, Flex: Discord Profile Badges Got an Upgrade

### Nitro’s Biggest Year Yet: A Look Back at 2026

![](/images/posts/95c08accee70.png)

### Discord Gift Cards: The Easiest Holiday Gift on Your List

![](/images/posts/ff1d1b462308.png)

### Making Content from Discoverable Servers Easier to Discover

![](/images/posts/4d3d0c1e9f37.png)

### Discord Update: October 22, 2026

### Discord Patch Notes: October 6, 2026

![](/images/posts/b5e6d8234d67.png)

### Cauldron Bubble w/o the Trouble? It’s Discord Halloween, Witches

![](/images/posts/dfde4ee7eade.png)

### Discord Update: September 25, 2026

![](/images/posts/dd1ffa0f76bb.png)

### Adding the Discord Updates YOU Want to See

### Discord Patch Notes: September 8, 2026

![](/images/posts/a53478fbc4bf.png)

### Link Discord and WoW to Keep the Guild Chatting Wherever You Are

![](/images/posts/1516f8b40ecc.png)

### Discord Update: August 11, 2026 Changelog

### Discord Patch Notes: August 4, 2026

![](/images/posts/e22521ba2d45.png)

### Squircles, Styles, and Spacing: How Your Feedback is Helping Improve Mobile

### Introducing Profile Frames: Decorative Borders to Make Your Discord Profile Museum-Worthy

### Discord Patch Notes: July 7, 2026

![](/images/posts/8980a292ba40.png)

### Discord is Now on Meta Quest: Reach Out to Your Servers While in VR

![](/images/posts/2d2b9414a624.png)

### Discord Update: June 25, 2026 Changelog

![](/images/posts/278c27289412.jpg)

### Introducing: You Bar

### Discord Patch Notes: June 4, 2026

![](/images/posts/35d84af06177.png)

### Official Discord Integrations for Steal a Brainrot, Grow a Garden, Brookhaven RP, and more

![](/images/posts/a0078a97d82e.png)

### Making It Easier Than Ever to Connect with Friends in League & VAL!

![](/images/posts/58822d187632.png)

### Every Voice and Video Call on Discord Is Now End-to-End Encrypted

### Nitro Now Comes with Xbox Game Pass and New Benefits. Welcome to Nitro Rewards.

![](/images/posts/0409445de3f9.png)

[翻译失败，原文如下]

### Stock Up in the New Rust Shop! Enjoy a Discord-Only 20% Sale on Most Items until 5/21

### Discord Patch Notes: April 6, 2026

### Discord Update: March 24, 2026 Changelog

### Discord Patch Notes: March 6, 2026

![](/images/posts/693ceb227192.png)

### How to Change Your Theme to Bring Your Vibe to Discord

### Discord Patch Notes: February 4, 2026

### Gift Ideas for the Dedicated Discord User in Your Life

### Your Discord Checkpoint is Rolling Out! Celebrate What You Did in 2025

### Save and Display Your Faves: Add Discord Shop & Marvel Rivals Items to Your Profile’s Wishlist

![](/images/posts/0cea5e682a99.png)

### Bringing In-Game Commerce to Discord Communities

![](/images/posts/5dc37847ea68.png)

### Discord Update: November 6, 2025 Changelog

![](/images/posts/94a276169cc6.png)

### A Cornucopia of Updates Make Discord on Desktop Fresher Than a Crisp Fall Breeze

### Discord Patch Notes: November 4, 2025

### Discord Patch Notes: October 7, 2025

### Discord Update: September 25, 2025 Changelog

### New Looks for Nitro, New Looks for You. Get Yourself a Nitro-exclusive Profile Bundle!

### Transforming Game Discovery with Instant Play Experiences on Discord

![](/images/posts/eca0f0241bb5.jpg)

### Reward Your Play: Complete Quests. Earn Orbs. Get Sweet Stuff.

### Discord Update: June 30, 2025 Changelog

![](/images/posts/f36afc7961d0.png)

### Get More From Your Boosts With New Server Perks

![](/images/posts/1ffee6646ab2.png)

### Gift Nitro and Earn A Flavorful Splash for your Avatar

![](/images/posts/235c51d590d1.png)

### Discord Social SDK Updates & Integrations

### Discord Patch Notes: June 3, 2025

![](/images/posts/a553192fb159.png)

### Go Beyond, Plus Ultra! with the My Hero Academia Collection

### STAR WARS™ Makes Its Way to Discord

### Discord Patch Notes: May 1, 2025

### Worthy of a Plaque: Nameplates Land in the Shop

![](/images/posts/f81a51eada93.png)

### Make More Closet Space! Nitro Members Can Now Keep Avatar Decoration Quest Rewards for Longer

### Discord Patch Notes: April 3, 2025

### Discord Update: March 25, 2025 Changelog

### Revamped Overlay & Refreshed Desktop Give Game Time a Boost

### Discord Patch Notes: March 11, 2025

### Discord Patch Notes: February 3, 2025

![](/images/posts/769b33700386.png)

### Discord Update: December 19, 2024 Changelog

### Discord Patch Notes: December 5, 2024

### Discord Update: November 18, 2024 Changelog

![](/images/posts/c408bb8b2bf9.png)

### Celebrate Arcane’s Second Season with a new Shop Collection

### Discord Patch Notes: November 1, 2024

### Set Out for a Discord Adventure! Check Out Our Roll20 Adventure & D&D Shop Collection

### Discord Patch Notes: October 1, 2024

### Discord Update: September 26, 2024 Changelog

![](/images/posts/979a60524f27.png)

### Discover More Ways to Play with Apps – Now Anywhere on Discord!

### Legacy Shop Favorites Emerge from The Vault for a First Anniversary Encore!

### Discord Patch Notes: August 30, 2024

### Discord Update: August 28, 2024 Changelog

![](/images/posts/42ba906c7ca4.png)

### Queue Up Your Playlists on Discord with the Amazon Music Listening Party Activity!

### Discord Patch Notes: August 1, 2024

![](/images/posts/3f621677150c.png)

### Now Available: See What’s Happening on Discord, Directly from your Xbox console

![](/images/posts/57474bf889e7.png)

### Discord Update: July 26, 2024 Changelog

### WHO LIVES ON YOUR PROFILE FOR ALL TO SEE? 🎶 SPONGEBOB, IN THE SHOP!

### Discord Patch Notes: July 1, 2024

### Discord Update: June 20, 2024 Changelog

![](/images/posts/26adccde45b3.jpg)

### How to Join Discord Calls Directly From Your PS5® — No Phone Needed!

![](/images/posts/84ce516c9413.png)

### Feast Your Monit-eyes on Today's Exciting Developer Updates!

### Discord Patch Notes: May 2024

![](/images/posts/f15e598ca5e8.png)

### Refining Discord’s Mobile Experience With Your Feedback

![](/images/posts/7f4e99e4bb8f.png)

### Discord Update: May 13, 2024 Changelog

### Discord Patch Notes: April 2024

![](/images/posts/1ef336a84bbf.png)

### Discord Update: April 3, 2024 Changelog

### Lock in. Stand out. VALORANT arrives in the Shop.

### Discord Update: March 5, 2024 Changelog

### Discord Update: December 13, 2023 Changelog

![](/images/posts/500f02d6a518.png)

### Improving Our Mobile Experience

![](/images/posts/8d372a01af79.png)

### Discord Update: October 19, 2023 Changelog

### Avatar Decorations & Profile Effects: Collect and Keep the Newest Styles

![](/images/posts/1f3039fb35b3.png)

### Discord Update: September 13, 2023 Changelog

### Now Available: Stream Your Xbox Games Directly to Discord

### Discord Update: July 29, 2023 Changelog

### Meme Up Some Fun with Remix

### Discord Update: June 22, 2023 Changelog

### Server Subscriptions Just Got Super Powered: Introducing Media Channels, Tier Templates and more!

### Discord Update: May 22, 2023 Changelog

### Evolving Usernames on Discord

### Discord Update: April 14, 2023 Changelog

### Welcome Your New Members Easily with Community Onboarding

---

> 本文由AI自动翻译，原文链接：[Discord <3 Linux: A Year of Upgrades](https://discord.com/blog/discord-linux-a-year-of-upgrades)
> 
> 翻译时间：2026-11-13 09:19
