
We back ../zahir2 as the monitoring system

**Communication**
- No sychophantic language please
- Use British English
- Do not remove my docstrings
- Do not delete comments, it's annoying. I use them to make it obvious what a block of code is intended to do

**Coding style**

- Python 3.14
- Functional programming
- Never use single-letter variables
- I name exceptions `err` and indices `idx`, `jdx`, etc.
- Functions must be short and single purpose.
- No mid file imports
- Avoid deeply nested lines
- use the constants file for constants. document with a plain english line comment what the thing represents. group constants in a block of related terms.
- Avoid deeply nested lines
- Do not write large functions. Split into subfunctions
- Do not write inner functions; use partial application instead
- Avoid using optional, or `X | None = None` unless there's a direct need for it
- Factor out complex type definitions into named type definitions.
- Add short descriptions to each file of the intent of the contents
- Factor out shared test setup code to a conftest.py
- All types live in `bookman_types.py` at the package root. Do not create per-subpackage type files.

**Testing**

- Do not attempt to run using Python -c, it will fail
- Use pytest
- Factor out test-data creation from test assertions
- Tests must have description strings like  "Proves <general system property>"
- ux tests should just be added by me, on request. Normally, create tests in tests/

**Tools & build**

- `rs` is my main build system
- Set up `uv`, `ruff`
- Always use `uv run python`, never `python` or `python3`
- Use `sqlite` CLI command, not `sqlite3`
