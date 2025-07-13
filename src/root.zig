const std = @import("std");
const c = @cImport({
    @cInclude("raylib.h");
});

pub export fn init() c_int {
    c.InitWindow(360, 480, "test");
    return 0; // Success
}

// --- 2. Event Polling Function ---
// This will be called repeatedly in a loop by Python.
// Returns `true` if the app should quit, `false` otherwise.
pub export fn poll_events() bool {
    c.PollInputEvents();
    return c.WindowShouldClose();
}

// --- 3. Shutdown Function ---
// This will be called once at the end.
pub export fn shutdown() void {
    std.log.info("byee", .{});
}
