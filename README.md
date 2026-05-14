# cursor-skills — Hướng dẫn

Repo cung cấp thư mục **`.cursor/`** (skills, rules, commands, agents, …) để **copy vào project** và dùng trong **Cursor**. Cấu trúc & cách dùng từng phần: **[`.cursor/README.md`](.cursor/README.md)**.

**Đã copy `.cursor/` vào repo đích?** Làm **Checklist** (bước 1→7).

---

## Lấy kit và copy

Từ máy bạn cần có thư mục `./.cursor/` (clone repo này hoặc copy từ monorepo).

```bash
rsync -a ./.cursor/ /đường/dẫn/project/.cursor/
```

*(Tuỳ chọn)* Gộp skill vào mọi project (`~/.cursor/skills/`): `./scripts/sync-skills-to-home.sh`.

---

## Checklist — sau khi copy

| # | Việc làm |
|---|----------|
| **1** | `.cursor/` nằm **ngay root** project (cùng cấp `.git` / `package.json`). `ls .cursor` có `skills`, `rules`, `commands`, … |
| **2** | **File → Open Folder** đúng root đó. Monorepo: mở app con có `.cursor/`, không mở cha. |
| **3** | Nếu đã mở project **trước** khi copy: **Developer: Reload Window**. |
| **4** | Bật **Agent** trong chat/Composer (khuyến nghị cho workflow `ck`). |
| **5** | Gõ **`/`** → thử `/ck-plan`, `/ck-cook`, … Lệnh phải là file **phẳng** `.cursor/commands/*.md` (thư mục con thường không hiện trong `/`). |
| **6** | **`@`** tới `.cursor/skills/.../SKILL.md` hoặc dùng slash trỏ tới skill đó. |
| **7** | Kiểm tra **Rules / project rules** có nguồn từ `.cursor/rules/*.mdc`. |

**Tuỳ chọn:** `python3 .cursor/_fix_skills_frontmatter.py` và `python3 .cursor/_mirror_paths.py` sau chỉnh tay; hook Python chỉ khi có `hooks.json` — [`.cursor/hooks/README.md`](.cursor/hooks/README.md).

---

## Slash gợi ý (`ck`)

| Slash | Mục đích |
|-------|----------|
| `/ck-brainstorm` | Ý tưởng / spec |
| `/ck-plan` | Kế hoạch triển khai |
| `/ck-cook` | Code theo plan |
| `/ck-fix` | Sửa lỗi có quy trình |
| `/ck-init` | Bootstrap `.cursor` sang repo khác |

---

## Sự cố thường gặp

- **Không thấy `/ck-*`:** sai workspace, thiếu reload, hoặc lệnh không nằm phẳng trong `commands/`.
- **Hook `.py` không chạy:** Cursor không gọi mặc định — cần cấu hình theo [docs Cursor](https://docs.cursor.com) + `hooks/README.md`.

---

## Trong repo `cursor-skills` (maintainer)

```bash
python3 scripts/verify_kit.py
```

Đồng bộ skill vào đây: `rsync -a …/.cursor/skills/ ./.cursor/skills/` rồi hai lệnh `python3 .cursor/_fix_skills_frontmatter.py` và `_mirror_paths.py`.

Ghi chú monorepo: [`CURSOR.md`](CURSOR.md).
