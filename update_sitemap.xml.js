import fs from "fs";
import path from "path";
import { SitemapStream } from "sitemap";

const hostname = "https://gobangol.lh520.pw";
const pagesDir = path.resolve("./src/pages");

// 递归获取页面路径
function getRoutes(dir, base = "") {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  let routes = [];

  for (const entry of entries) {
    if (entry.isDirectory()) {
      routes = routes.concat(
        getRoutes(path.join(dir, entry.name), path.join(base, entry.name))
      );
    } else if (entry.isFile() && entry.name.endsWith(".vue")) {
      let routePath = path.join(base, entry.name.replace(/\.vue$/, ""));
      if (routePath.endsWith("/index")) {
        routePath = routePath.replace(/\/index$/, "");
      }
      routes.push(routePath === "" ? "/" : `/${routePath.replace(/\\/g, "/")}`);
    }
  }

  return routes;
}

const routePaths = getRoutes(pagesDir);

// 创建 sitemap 流
const sitemap = new SitemapStream({ hostname });
const writeStream = fs.createWriteStream("./dist/sitemap.xml");

sitemap.pipe(writeStream);

// 写入每条路由
routePaths.forEach((url) =>
  sitemap.write({ url, changefreq: "weekly", priority: 0.8 })
);

// 结束流
sitemap.end();

// 监听完成
writeStream.on("finish", () => {
  console.log("✅ sitemap.xml 已生成！");
});
