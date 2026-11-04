# Definition of Done

A ticket is **Done** only when every item below is true.

## Every ticket
- [ ] All acceptance criteria are met
- [ ] Code is committed to `main` with the ticket ID in the message (e.g. `B1.001: lock portfolio row`)
- [ ] No new warnings or errors when the server starts
- [ ] `tests/test_main.http` updated if an endpoint was added or changed

## When the schema changes
- [ ] Alembic migration has a working `upgrade()` **and** `downgrade()`
- [ ] Migration applied on Supabase

## Testing
- [ ] **From Sprint 2 on:** pytest covers the acceptance criteria and `pytest` passes
- [ ] **Sprint 1 only:** verified manually using the `.http` file or a script (pytest isn't set up yet)

## Wrap-up
- [ ] Ticket status updated in the sprint file, ACTUAL hours filled in
- [ ] Anything worth remembering written in `devlog.md`