const std = @import("std");

pub fn build(b: *std.Build) !void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // --- 1. Set up the Raylib Dependency as a Shared Library (DLL) ---
    const raylib_dep = b.dependency("raylib_zig", .{
        .target = target,
        .optimize = optimize,
        // CRUCIAL: Tell the dependency to build a shared library (.dll)
        // instead of a static one (.lib).
        .shared = true,
    });

    // This will now install the raylib.dll to the output directory.
    b.installArtifact(raylib_dep.artifact("raylib"));

    // --- 2. Dynamically Build a DLL for Each .zig File in 'src' ---
    var src_dir = try std.fs.cwd().openDir("src", .{ .iterate = true });
    defer src_dir.close();

    var dir_iterator = src_dir.iterate();
    while (try dir_iterator.next()) |entry| {
        // Process only .zig files
        if (entry.kind != .file or !std.mem.endsWith(u8, entry.name, ".zig")) {
            continue;
        }

        const lib_name = std.fs.path.stem(entry.name);
        const root_source_path = b.pathJoin(&.{ "src", entry.name });

        std.log.info("Building script: {s} -> {s}.dll", .{ entry.name, lib_name });

        const script_dll = b.addSharedLibrary(.{
            .name = lib_name,
            .root_source_file = b.path(root_source_path),
            .target = target,
            .optimize = optimize,
        });

        // Add the raylib module so you can @import("raylib") in your scripts.
        script_dll.root_module.addImport("raylib", raylib_dep.module("raylib"));

        // This now links your script DLL against the main raylib DLL.
        script_dll.linkLibrary(raylib_dep.artifact("raylib"));

        b.installArtifact(script_dll);
    }
}
