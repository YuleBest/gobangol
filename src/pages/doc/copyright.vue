<template>
  <div class="main">
    <div class="links">
      <v-btn to="/">返回首页</v-btn>
      <v-btn to="https://github.com/YuleBest/gobangol" target="_blank"
        >前往 GitHub</v-btn
      >
    </div>
    <div class="license">
      <h2>许可证 | License</h2>
      <pre>
Yule License 1.0.0
==================

中文版（Chinese Version）
------------------------
版权所有 (c) 2025 Yule

特此免费授予任何获得本软件及相关文档文件（以下简称“软件”）副本的人，
在遵守以下条件的前提下，无限制地使用本软件，包括复制、修改、合并、发布、分发、展示和演示本软件的权限，

但明确禁止将本软件用于任何商业目的（包括但不限于盈利性销售、商业服务、广告及其它任何商业活动）。

上述版权声明和本许可声明应包含在本软件的所有副本或重要部分中。

本软件按“原样”提供，不提供任何形式的明示或暗示保证，包括但不限于适销性、特定用途适用性和不侵权的保证。
在任何情况下，版权持有人或版权授权人均不对因本软件或软件的使用或其他交易产生的任何索赔、损害或其他责任承担责任，无论是在合同诉讼中，侵权诉讼中或其他方面。

---

English Version
---------------

Copyright (c) 2025 Yule

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,

**subject to the following restriction: the Software shall NOT be used for any commercial purposes** (including but not limited to commercial sale, commercial services, advertising, or any other commercial activity).

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    </pre
      >
    </div>
    <div class="reference">
      <h2>参考引用 | Reference</h2>
      <pre>
- 本站所引用的可爱勋章，包括：
  - 页脚的 Github、TypeScript、Vue，404 页面的 404NotFound：SAWARATSUKI's license, SAWARATSUKI create a new repository for KawaiiLogos. The full list of logos is available in the repository. The logos not in this repository is temporary following license CC BY 4.0. （Link: https://github.com/SAWARATSUKI/KawaiiLogos ），特别感谢 SAWARATSUKI 创作的可爱勋章！
- 访问量与访问人数统计：不蒜子（ https://www.busuanzi.cc/ ），特别感谢不蒜子提供的免费访问量与访问人数统计！
- SSL 安全认证签章：TrustSSL（ https://www.trustssl.cc/ ），特别感谢 TrustSSL 提供的 SSL 安全认证签章！
    </pre
      >
    </div>
  </div>
</template>

<style>
.main {
  margin: 20px;
}

.links * {
  margin-right: 10px;
  padding: 0 0 0 5px;
}

.main pre {
  font-size: 14px;
  max-width: 80vw;
  overflow-x: auto;
  white-space: pre;
}

.main h2 {
  margin-top: 20px;
}
</style>

<script setup>
import { useHead } from "@vueuse/head";
useHead({
  title: "版权声明 - GoBang OL",
  meta: [{ name: "description", content: "GoBang OL 版权声明" }],
});
</script>
