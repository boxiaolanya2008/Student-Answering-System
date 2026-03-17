# SVG 图标使用指南

## 📁 图标文件目录

```
static/icons/
├── logo.svg        # Logo 图标（书本形状）
├── document.svg    # 文档图标（空状态用）
├── camera.svg      # 相机图标（上传用）
└── queue.svg       # 队列图标（排队状态用）
```

## 🎨 图标设计理念

所有图标采用统一的设计语言：
- **风格**: Material Design + 扁平化
- **圆角**: 统一的圆角处理（2px）
- **渐变**: 线性渐变填充（45 度角）
- **描边**: 2px 描边宽度
- **颜色**: 蓝色系为主色调

## 💻 使用方法

### 1. 在 HTML 中直接使用

```html
<!-- Logo 图标 -->
<div class="logo-icon">
    <img src="/static/icons/logo.svg" alt="Logo">
</div>

<!-- 文档图标 -->
<div class="empty-state-icon">
    <img src="/static/icons/document.svg" alt="Document">
</div>

<!-- 相机图标 -->
<div class="dropzone-icon">
    <img src="/static/icons/camera.svg" alt="Camera">
</div>
```

### 2. CSS 样式配合

```css
.icon-container {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-container svg,
.icon-container img {
    width: 28px;
    height: 28px;
}

/* 大图标 */
.large-icon {
    width: 80px;
    height: 80px;
}

.large-icon svg,
.large-icon img {
    width: 48px;
    height: 48px;
}
```

### 3. 内联 SVG（可选）

如果需要更灵活的控制，可以直接嵌入 SVG 代码：

```html
<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- SVG 内容 -->
</svg>
```

## 🎯 图标规格

### Logo 图标 (logo.svg)
- **尺寸**: 40x40 px
- **内容**: 书本形状
- **用途**: 导航栏、登录页
- **颜色**: 白色描边，透明背景

### 文档图标 (document.svg)
- **尺寸**: 80x80 px
- **内容**: 文档列表
- **用途**: 空状态提示
- **颜色**: 蓝紫色渐变背景，深色描边

### 相机图标 (camera.svg)
- **尺寸**: 64x64 px
- **内容**: 相机形状
- **用途**: 图片上传区域
- **颜色**: 蓝白渐变背景，蓝色描边

### 队列图标 (queue.svg)
- **尺寸**: 80x80 px
- **内容**: 队列列表
- **用途**: 排队状态页面
- **颜色**: 蓝色渐变背景，深色描边

## 🎨 自定义图标

如需添加新图标，请遵循以下规范：

1. **尺寸规范**
   - 小图标：40x40 px
   - 中图标：64x64 px
   - 大图标：80x80 px

2. **设计规范**
   - 使用统一的圆角（2px）
   - 描边宽度：2px
   - 渐变角度：45 度
   - 颜色：蓝色系

3. **文件格式**
   - 格式：SVG 1.1
   - 编码：UTF-8
   - 压缩：可选

4. **命名规范**
   - 使用小写字母
   - 单词间用下划线分隔
   - 语义清晰

## 📊 性能优化

1. **SVG 压缩**
   - 移除不必要的元数据
   - 简化路径点
   - 复用渐变定义

2. **缓存策略**
   - 设置长期缓存头
   - 使用版本号控制更新

3. **响应式支持**
   - 使用 viewBox 确保缩放
   - CSS 控制实际显示尺寸

## ✅ 优势对比

### SVG vs Emoji

| 特性 | SVG | Emoji |
|------|-----|-------|
| 可定制性 | ✅ 完全可控 | ❌ 系统依赖 |
| 一致性 | ✅ 跨平台一致 | ❌ 平台差异大 |
| 可访问性 | ✅ 支持 alt 文本 | ⚠️ 部分支持 |
| 性能 | ✅ 矢量无损 | ✅ 字体渲染 |
| 文件大小 | ✅ 较小 | ✅ 更小 |
| 动画支持 | ✅ CSS/SVG 动画 | ❌ 不支持 |

## 🔧 工具推荐

### 图标编辑工具
- **Figma**: 在线设计工具
- **Inkscape**: 免费开源 SVG 编辑器
- **Adobe Illustrator**: 专业矢量工具

### SVG 优化工具
- **SVGO**: SVG 压缩工具
- **SVGOMG**: 在线 SVG 优化器

## 📝 注意事项

1. **兼容性**: 所有现代浏览器都支持 SVG
2. **可访问性**: 始终提供 `alt` 属性
3. **颜色对比**: 确保符合 WCAG 标准
4. **响应式**: 使用相对单位确保缩放

---

**最后更新**: 2026 年 3 月 17 日
