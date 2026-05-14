# Hướng dẫn cài đặt & sử dụng — cursor-skills

Repo này cung cấp một thư mục **`.cursor/`** (skills, rules, commands, agents, …) để bạn **copy vào bất kỳ project nào** và dùng trong **Cursor**. Tài liệu dưới đây là **setup guide** từng bước.

---

## Bạn sẽ có gì sau khi cài?

| Thành phần | Vai trò |
|------------|---------|
| `.cursor/skills/` | Skill dạng `tên-skill/SKILL.md` (frontmatter `name`, `description`). |
| `.cursor/rules/` | Rule Cursor (`.mdc`, có `globs` / `alwaysApply`). |
| `.cursor/commands/*.md` | Slash command project: tên lệnh = tên file bỏ `.md` (vd. `ck-cook.md` → **`/ck-cook`**). Giữ file **phẳng** trong `commands/` — Cursor thường **không** liệt kê lệnh trong thư mục con. |
| `.cursor/agents/`, `contexts/`, `coding-levels/` | Prompt / ngữ cảnh tham chiếu cho agent. |
| `.cursor/hooks/` | Script Python (gốc Claude Code) — **tùy chọn**, xem mục [Hooks](#phần-bổ-sung-hooks-tùy-chọn). |

---

## Điều kiện bắt buộc (đọc trước khi cài)

1. **Workspace trong Cursor** phải là **thư mục gốc của chính project** — tức thư mục **trực tiếp chứa** `.cursor/` (cùng cấp với `.git`, `package.json`, …).
2. Nếu bạn mở **monorepo** ở thư mục cha, trong khi `.cursor/` chỉ nằm trong `apps/web/`, thì phải **File → Open Folder → `apps/web`** (hoặc copy `.cursor/` lên đúng root bạn đang mở).

---

## Phần 1 — Chuẩn bị bản kit

**Cách A — Clone repo `cursor-skills`**

```bash
git clone <url-repo-cursor-skills> cursor-skills
cd cursor-skills
```

**Cách B — Đã có sẵn trong monorepo (ví dụ Claude-kit)**

Đường dẫn ví dụ: `…/Claude-kit/cursor-skills/`. Mọi lệnh dưới đây giả sử bạn đang đứng tại **thư mục gốc của repo `cursor-skills`** (nơi có thư mục con `.cursor/`).

---

## Phần 2 — Cài kit vào repo đích

### Bước 2.1 — Copy toàn bộ `.cursor/`

Từ **gốc repo `cursor-skills`** (có `./.cursor/`):

```bash
rsync -a ./.cursor/ /đường/dẫn/tới/repo-của-bạn/.cursor/
```

Hoặc dùng Finder / Explorer: copy nguyên thư mục `.cursor` vào root project.

### Bước 2.2 — (Tuỳ chọn) Chỉ đồng bộ **skills** vào thư mục user Cursor

Dùng khi bạn muốn skill có mặt **mọi project** (global), không chỉ một repo:

```bash
cd /đường/dẫn/tới/cursor-skills
./scripts/sync-skills-to-home.sh
```

Mặc định gộp vào `~/.cursor/skills/`. Đổi đích:

```bash
CURSOR_USER_SKILLS_DIR="$HOME/.cursor/skills" ./scripts/sync-skills-to-home.sh
```

---

## Phần 3 — Mở project trong Cursor

1. Mở **Cursor**.
2. **File → Open Folder…**
3. Chọn **`/đường/dẫn/tới/repo-của-bạn`** (folder đã có `.cursor/` sau bước 2).

Không mở nhầm thư mục cha nếu `.cursor/` không nằm ở đó.

---

## Phần 4 — Kiểm tra nhanh sau khi setup

1. **Rules** — Trong Cursor, mở phần Rules / Project rules (theo phiên bản Cursor) và xác nhận có rule dưới `.cursor/rules/*.mdc`.
2. **Skills** — Thử `@` hoặc skill picker (nếu bản Cursor của bạn hỗ trợ) với tên skill trong `.cursor/skills/` (ví dụ `ck-plan`, `code-review`).
3. **Commands** — Trong ô chat / Composer, gõ **`/`** rồi tìm lệnh có tên file (vd. **`/ck-cook`**, **`/ck-plan`**, **`/ck-init`**).  
   - Các file nằm **phẳng** trong `.cursor/commands/` dạng `ck-*.md` để Cursor nhận (thư mục con `ck/` thường **không** hiện trong menu `/`).

Chi tiết kỹ thuật và giới hạn (hooks, workspace): [`.cursor/README.md`](.cursor/README.md).

---

## Kiểm tra tự động (agents, commands, hooks)

Trong repo `cursor-skills`, chạy:

```bash
python3 scripts/verify_kit.py
```

Script kiểm tra:

| Hạng mục | Việc làm |
|----------|----------|
| **Agents** (`agents/*.md`) | Có frontmatter YAML `---`; nội dung không quá mỏng. |
| `.cursor/commands/**/*.md` | Có `---` đầu file; cảnh báo nếu còn chuỗi `.claude/`. |
| **Skills** (`skills/**/SKILL.md`) | Mọi `SKILL.md` (kể cả thư mục con) đều có frontmatter. |
| **Hooks** (`hooks/**/*.py`) | Parse cú pháp Python (`ast`); chạy **smoke** từng entry script với stdin tối thiểu (exit 0 hoặc 2 = chấp nhận). |
| **Portability** | Cảnh báo nếu hook vẫn đọc `.claude/contexts` hoặc `.claude/session-data` (xem output WARN). |

**Giới hạn:** không thể xác nhận từ CLI rằng **Cursor** đã load rule/command trong UI — cần mở project trong Cursor và thử thủ công (mục Phần 4). Hooks Python **không** được Cursor gọi trừ khi bạn cấu hình `hooks.json`.

---

## Phần 5 — Dùng workflow `ck` (tóm tắt)

Sau khi mở đúng workspace:

| Mục đích | Gợi ý |
|----------|--------|
| Lên ý tưởng / spec trước khi code | **`/ck-brainstorm`** → `.cursor/skills/ck-brainstorm/SKILL.md`. |
| Lập kế hoạch triển khai | **`/ck-plan`** → `.cursor/skills/ck-plan/SKILL.md`. |
| Code theo plan | **`/ck-cook`** → `.cursor/skills/ck-cook/SKILL.md`. |
| Sửa lỗi có quy trình | **`/ck-fix`** → `.cursor/skills/ck-fix/SKILL.md`. |
| Bootstrap `.cursor` sang project khác | **`/ck-init`** → `.cursor/commands/ck-init.md`. |

Nội dung cụ thể nằm trong từng file `SKILL.md` / command — agent sẽ đọc path **tương đối** `.cursor/...` trong repo bạn.

---

## Phần bổ sung: Hooks (tuỳ chọn)

- Thư mục `.cursor/hooks/*.py` xuất phát từ **Claude Code**, nhiều chỗ vẫn tham chiếu `.claude/` / session kiểu Claude.
- **Cursor** dùng file **`hooks.json`** và [giao thức hook riêng](https://docs.cursor.com). Kit **không** bật hook Python tự động sau khi copy.
- Đọc thêm: [`.cursor/hooks/README.md`](.cursor/hooks/README.md).

---

## Phần dành cho người maintain kit (monorepo Claude-kit)

Nếu bạn vừa chỉnh skill trong **`my-skills/.claude/skills/`** và muốn đồng bộ vào repo này rồi chuẩn hoá frontmatter / path:

```bash
cd /đường/dẫn/tới/cursor-skills
rsync -a ../my-skills/.claude/skills/ ./.cursor/skills/
python3 ./.cursor/_fix_skills_frontmatter.py
python3 ./.cursor/_mirror_paths.py
```

Điều chỉnh `../my-skills` cho đúng cây thư mục máy bạn. Người dùng **chỉ copy `.cursor/`** không cần monorepo.

---

## Xử lý sự cố thường gặp

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|------------|-------------------------|------------|
| Không thấy skill / rule | Mở sai workspace (cha thay vì con có `.cursor/`). | Open Folder đúng root chứa `.cursor/`. |
| Command không chạy đúng | Path tương đối `.cursor/...` không tồn tại tại root đang mở. | Kiểm tra `ls .cursor/skills` tại root workspace. |
| Hook Python không chạy | Cursor không dùng `settings.json` kiểu Claude. | Bỏ qua hoặc tự viết `hooks.json` + chỉnh script. |

---

## Tài liệu liên quan trong repo

| File | Nội dung |
|------|----------|
| [`scripts/verify_kit.py`](scripts/verify_kit.py) | Kiểm tra tự động agents / commands / skills / hooks. |
| [`.cursor/README.md`](.cursor/README.md) | Portable kit, bảng thành phần, bảo trì script. |
| [`CURSOR.md`](CURSOR.md) | Gợi ý ngắn khi dùng cùng monorepo `Claude-kit`. |
| [`my-skills/CLAUDE.md`](../my-skills/CLAUDE.md) | Bộ `.claude` (Claude Code) tương ứng — chỉ khi bạn có monorepo. |

---

## Tóm tắt một dòng

**Copy `./.cursor/` vào root repo → mở đúng folder đó trong Cursor → dùng skills / rules / commands theo từng file trong `.cursor/`.**
