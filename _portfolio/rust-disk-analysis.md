---
title: "Disk usage analyser"
order: 4
excerpt: "A desktop app written in Rust that shows what is filling up a disk and finds duplicate files."
---

A desktop app that scans a disk, shows what takes up space, and finds duplicate
files by comparing their contents. It is written in Rust with a Tauri interface,
and it shows progress while the scan runs. You choose what to delete; the app
doesn't delete anything on its own.
