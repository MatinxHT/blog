{
  "title": "Why Is It So Hard to Skip Microsoft Account Sign-In During Windows Setup?",
  "date": "2026-10-11T00:00:00+08:00",
  "draft": false,
  "type": "post",
  "slug": "windows-10-22h2-local-account-oobe",
  "description": "Resetting an old Windows 10 22H2 laptop turned into a struggle with Microsoft account sign-in. Creating a local administrator account and rebooting finally worked.",
  "tags": ["Windows 10", "Microsoft Account", "Local Account", "OOBE"],
  "categories": ["Deployment and Operations"]
}

I recently reset an old laptop running Windows 10 22H2. During setup, Windows kept insisting that I sign in with a Microsoft account before I could continue. Cortana also made an unwelcome appearance.

All I wanted was a local account, because I was preparing the laptop for sale. I tried several workarounds, including `nothankyou`, without success. What eventually worked was creating a local user from the command prompt and restarting the computer.

## What I tried first

At the Microsoft account sign-in screen in the out-of-box experience (OOBE), I pressed `Shift + F10` to open a command prompt.

ChatGPT initially suggested three approaches:

- Run `OOBE\BYPASSNRO` to try to bypass the network requirement.
- Disconnect from the network, including trying `ipconfig /release`, then go back a screen and look for an offline setup option.
- Run `start ms-cxh:localonly` to try to open the local account creation dialog directly.

None of them worked on this laptop.

## Creating the account directly

I stopped looking for an offline option in the setup interface and tried creating a local user directly:

```cmd
net user LocalUser * /add
net localgroup Administrators LocalUser /add
```

`LocalUser` is a placeholder; replace it with your preferred username and use the same name in both commands. The first command creates the user and prompts you to enter and confirm a password. Nothing appears on screen while you type the password. The second command adds the user to the local Administrators group.

After creating the account, I followed the next steps from the conversation and ran:

```cmd
cd /d %windir%\system32\oobe
msoobe.exe
```

The screen got stuck at “Please wait.” At that point, I thought this attempt had failed too. Eventually, I stopped waiting and restarted the computer:

```cmd
shutdown /r /t 0
```

After the restart, I could sign in with the local account I had just created. That finally resolved the problem.

## Why this frustrates me

If Windows can accept a locally created account and let me use the operating system normally, why does Microsoft make the setup process so difficult? These extra hurdles only damage the way people feel about Windows.

I spent 15 years as a Microsoft community enthusiast, regularly discussing technology with Microsoft MVPs. Over the past five years, though, I have seen little from Microsoft that has excited the people in my circle. For the Chinese Microsoft community I knew, the release of Windows 10 felt like a high point.

I recognize the effort that has gone into Windows 11, especially its backward compatibility with software dating back to the Windows 98 era. But the overall experience of using Windows has become deeply frustrating. First, I saw many MVPs switch to macOS as their primary operating system. Eventually, I made the same move.

I can accept an initial online check to confirm that a machine is not locked to a previous owner's account. So far, Apple has not forced me to sign in with an Apple ID just to use macOS. Microsoft's insistence on pushing a Microsoft account during setup is infuriating, especially when a local account is all I need.

To me, this also reflects a broader lack of direction within Microsoft. Even in 2026, I do not feel that Microsoft can give developers a clear answer about which framework they should use to build Windows applications. The state of WinUI 3 worries me. WPF remains the veteran that keeps getting called in to keep things running, but these days it hardly lives up to the “Presentation” in its name.
