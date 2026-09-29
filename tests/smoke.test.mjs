import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const html = fs.readFileSync("index.html", "utf8");

test("production entry point exists", () => {
  assert.match(html, /<title>AudiQ/);
  assert.match(html, /id="analyze"/);
  assert.match(html, /id="verify"/);
  assert.match(html, /id="reportBtn"/);
});

test("manual verification gate exists", () => {
  assert.match(html, /All values are candidates/);
  assert.match(html, /Verify every point/);
});

test("experimental dependency is pinned", () => {
  assert.match(html, /docs\.opencv\.org\/4\.12\.0\/opencv\.js/);
});
