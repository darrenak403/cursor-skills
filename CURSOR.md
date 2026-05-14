# Ghi chú monorepo (Claude-kit)

Nếu bạn đang dùng cả **`Claude-kit/my-skills`** (Claude Code) và repo này:

- Bộ Cursor chính nằm tại **`cursor-skills/.cursor/`** trong monorepo.
- Hướng dẫn đầy đủ (setup từng bước): **[`README.md`](README.md)**.

Copy nhanh vào app khác:

```bash
rsync -a /path/to/Claude-kit/cursor-skills/.cursor/ /path/to/your-app/.cursor/
```

Tuỳ chọn: trong `my-skills` tạo symlink `ln -s ../cursor-skills/.cursor .cursor` nếu muốn mở `my-skills` mà vẫn thấy kit Cursor (cân nhắc trùng với `.cursor` riêng của project).
