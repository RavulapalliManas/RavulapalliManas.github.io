---
title: "High-performance disk analysis tool"
order: 4
meta: "Asynchronous Rust, with a Tauri interface"
excerpt: "An asynchronous Rust application that traverses file systems, visualises disk usage, and finds duplicates by cryptographic hash."
tags:
  - Rust
  - Tauri
  - Systems
---

An asynchronous Rust application that traverses file systems, visualises disk
usage, and detects duplicate files by cryptographic hash.

The interface is built with Tauri, and reports progress in real time while the
scan runs. Cleanup is interactive rather than automatic.
