import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

interface WechatConfig {
  appId: string;
  appSecret: string;
}

interface AccessTokenResponse {
  access_token?: string;
  errcode?: number;
  errmsg?: string;
}

interface UploadResponse {
  media_id: string;
  url: string;
  errcode?: number;
  errmsg?: string;
}

interface PublishResponse {
  media_id?: string;
  errcode?: number;
  errmsg?: string;
}

interface ArticleData {
  title: string;
  author?: string;
  digest?: string;
  content: string;
  thumbMediaId: string;
}

const TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token";
const UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material";
const DRAFT_URL = "https://api.weixin.qq.com/cgi-bin/draft/add";

function loadEnvFile(envPath: string): Record<string, string> {
  const env: Record<string, string> = {};
  if (!fs.existsSync(envPath)) return env;

  const content = fs.readFileSync(envPath, "utf-8");
  for (const line of content.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx > 0) {
      const key = trimmed.slice(0, eqIdx).trim();
      let value = trimmed.slice(eqIdx + 1).trim();
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      env[key] = value;
    }
  }
  return env;
}

function loadConfig(): WechatConfig {
  const cwdEnvPath = path.join(process.cwd(), ".baoyu-skills", ".env");
  const homeEnvPath = path.join(os.homedir(), ".baoyu-skills", ".env");

  const cwdEnv = loadEnvFile(cwdEnvPath);
  const homeEnv = loadEnvFile(homeEnvPath);

  const appId = process.env.WECHAT_APP_ID || cwdEnv.WECHAT_APP_ID || homeEnv.WECHAT_APP_ID;
  const appSecret = process.env.WECHAT_APP_SECRET || cwdEnv.WECHAT_APP_SECRET || homeEnv.WECHAT_APP_SECRET;

  if (!appId || !appSecret) {
    throw new Error(
      "Missing WECHAT_APP_ID or WECHAT_APP_SECRET.\n" +
      "Set via environment variables or in .baoyu-skills/.env file."
    );
  }

  return { appId, appSecret };
}

async function fetchAccessToken(appId: string, appSecret: string): Promise<string> {
  const url = `${TOKEN_URL}?grant_type=client_credential&appid=${appId}&secret=${appSecret}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch access token: ${res.status}`);
  }
  const data = await res.json() as AccessTokenResponse;
  if (data.errcode) {
    throw new Error(`Access token error ${data.errcode}: ${data.errmsg}`);
  }
  if (!data.access_token) {
    throw new Error("No access_token in response");
  }
  return data.access_token;
}

async function uploadImage(
  imagePath: string,
  accessToken: string
): Promise<UploadResponse> {
  let fileBuffer: Buffer;
  let filename: string;
  let contentType: string;

  if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
    const response = await fetch(imagePath);
    if (!response.ok) {
      throw new Error(`Failed to download image: ${imagePath}`);
    }
    const buffer = await response.arrayBuffer();
    if (buffer.byteLength === 0) {
      throw new Error(`Remote image is empty: ${imagePath}`);
    }
    fileBuffer = Buffer.from(buffer);
    const urlPath = imagePath.split("?")[0];
    filename = path.basename(urlPath) || "image.jpg";
    contentType = response.headers.get("content-type") || "image/jpeg";
  } else {
    const resolvedPath = path.isAbsolute(imagePath)
      ? imagePath
      : path.resolve(process.cwd(), imagePath);

    if (!fs.existsSync(resolvedPath)) {
      throw new Error(`Image not found: ${resolvedPath}`);
    }
    const stats = fs.statSync(resolvedPath);
    if (stats.size === 0) {
      throw new Error(`Local image is empty: ${resolvedPath}`);
    }
    fileBuffer = fs.readFileSync(resolvedPath);
    filename = path.basename(resolvedPath);
    const ext = path.extname(filename).toLowerCase();
    const mimeTypes: Record<string, string> = {
      ".jpg": "image/jpeg",
      ".jpeg": "image/jpeg",
      ".png": "image/png",
      ".gif": "image/gif",
      ".webp": "image/webp",
    };
    contentType = mimeTypes[ext] || "image/jpeg";
  }

  const boundary = `----WebKitFormBoundary${Date.now().toString(16)}`;
  const header = [
    `--${boundary}`,
    `Content-Disposition: form-data; name="media"; filename="${filename}"`,
    `Content-Type: ${contentType}`,
    "",
    "",
  ].join("\r\n");
  const footer = `\r\n--${boundary}--\r\n`;

  const headerBuffer = Buffer.from(header, "utf-8");
  const footerBuffer = Buffer.from(footer, "utf-8");
  const body = Buffer.concat([headerBuffer, fileBuffer, footerBuffer]);

  const url = `${UPLOAD_URL}?access_token=${accessToken}&type=image`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": `multipart/form-data; boundary=${boundary}`,
    },
    body,
  });

  const data = await res.json() as UploadResponse;
  if (data.errcode && data.errcode !== 0) {
    throw new Error(`Upload failed ${data.errcode}: ${data.errmsg}`);
  }

  if (data.url?.startsWith("http://")) {
    data.url = data.url.replace(/^http:\/\//i, "https://");
  }

  return data;
}

function parseFrontmatter(content: string): { frontmatter: Record<string, string>; body: string } {
  const frontmatter: Record<string, string> = {};
  let body = content;

  const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
  if (fmMatch) {
    const fmContent = fmMatch[1];
    body = fmMatch[2];

    for (const line of fmContent.split("\n")) {
      const colonIdx = line.indexOf(":");
      if (colonIdx > 0) {
        const key = line.slice(0, colonIdx).trim();
        let value = line.slice(colonIdx + 1).trim();
        value = value.replace(/^["'](.*)["']$/, "$1");
        frontmatter[key] = value;
      }
    }
  }

  return { frontmatter, body };
}

function extractTitleFromMd(content: string): string {
  const parsed = parseFrontmatter(content);
  if (parsed.frontmatter.title) return parsed.frontmatter.title;
  
  const h1Match = parsed.body.match(/^#\s+(.+)$/m);
  if (h1Match) return h1Match[1].trim();
  
  const h2Match = parsed.body.match(/^##\s+(.+)$/m);
  if (h2Match) return h2Match[1].trim();
  
  return "";
}

function extractDigestFromMd(content: string): string {
  const parsed = parseFrontmatter(content);
  if (parsed.frontmatter.digest) return parsed.frontmatter.digest;
  if (parsed.frontmatter.summary) return parsed.frontmatter.summary;
  if (parsed.frontmatter.description) return parsed.frontmatter.description;
  
  // Extract first paragraph
  const lines = parsed.body.split("\n").filter(line => line.trim() && !line.startsWith("#") && !line.startsWith("-") && !line.startsWith("*"));
  if (lines.length > 0) {
    const firstPara = lines[0].trim();
    return firstPara.length > 120 ? firstPara.slice(0, 117) + "..." : firstPara;
  }
  
  return "";
}

function renderMarkdownToHtml(mdPath: string): string {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const scriptsDir = __dirname;
  
  // Call md-to-wechat.ts to convert markdown
  const result = spawnSync(process.execPath, [
    path.join(scriptsDir, "md-to-wechat.ts"),
    mdPath,
    "--theme", "modern",
    "--cite"
  ], { 
    cwd: path.dirname(mdPath),
    encoding: "utf-8"
  });
  
  if (result.status !== 0) {
    throw new Error(`Failed to render ${mdPath}: ${result.stderr}`);
  }
  
  return result.stdout.trim();
}

async function processArticle(mdPath: string, thumbMediaId: string, accessToken: string): Promise<ArticleData> {
  console.error(`[wechat-batch-api] Processing: ${path.basename(mdPath)}`);
  
  const content = fs.readFileSync(mdPath, "utf-8");
  const title = extractTitleFromMd(content);
  let digest = extractDigestFromMd(content);
  const author = "岸叔";
  
  if (digest.length > 120) {
    digest = digest.slice(0, 117) + "...";
  }
  
  if (!title) {
    throw new Error(`No title found in ${mdPath}`);
  }
  
  // Render markdown to HTML using md-to-wechat.ts
  const __filename2 = fileURLToPath(import.meta.url);
  const __dirname2 = path.dirname(__filename2);
  const scriptsDir2 = __dirname2;
  
  // Call md-to-wechat.ts to convert markdown
  const result2 = spawnSync(process.execPath, [
    path.join(scriptsDir2, "md-to-wechat.ts"),
    mdPath,
    "--theme", "modern",
    "--cite"
  ], { 
    cwd: path.dirname(mdPath),
    encoding: "utf-8"
  });
  
  if (result2.status !== 0) {
    throw new Error(`Failed to render ${mdPath}: ${result2.stderr}`);
  }
  
  // Parse the JSON output to get the HTML path
  let htmlPath: string;
  try {
    const output = result2.stdout.trim();
    // Find the JSON part in the output (after the log messages)
    const jsonMatch = output.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      htmlPath = parsed.htmlPath;
    } else {
      throw new Error("No JSON output found");
    }
  } catch (e) {
    // Fallback: try the default HTML path
    htmlPath = mdPath.replace(/\.md$/i, ".html");
  }
  
  if (!fs.existsSync(htmlPath)) {
    throw new Error(`HTML file not generated: ${htmlPath}`);
  }
  
  const htmlContent = fs.readFileSync(htmlPath, "utf-8");
  
  return {
    title,
    author,
    digest,
    content: htmlContent,
    thumbMediaId,
  };
}

async function publishDrafts(articles: ArticleData[], accessToken: string): Promise<string> {
  const draftArticles = articles.map(article => {
    const draftArticle: any = {
      article_type: "news",
      title: article.title,
      content: article.content,
      thumb_media_id: article.thumbMediaId,
      need_open_comment: 1,
      only_fans_can_comment: 0,
    };
    if (article.author) {
      draftArticle.author = article.author;
    }
    if (article.digest) {
      draftArticle.digest = article.digest;
    }
    return draftArticle;
  });
  
  const res = await fetch(`${DRAFT_URL}?access_token=${accessToken}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ articles: draftArticles }),
  });
  
  const data = await res.json() as PublishResponse;
  if (data.errcode && data.errcode !== 0) {
    throw new Error(`Publish failed ${data.errcode}: ${data.errmsg}`);
  }
  
  if (!data.media_id) {
    throw new Error("No media_id in response");
  }
  
  return data.media_id;
}

const DEFAULT_COVER_URL = "https://qiniu.mpc6.com/2026/640.jpg"; // Default cover image URL
const MEDIA_ID_CACHE_FILE = path.join(os.homedir(), ".baoyu-skills", "thumb_media_id.cache");

function loadCachedThumbMediaId(): string | null {
  try {
    if (fs.existsSync(MEDIA_ID_CACHE_FILE)) {
      return fs.readFileSync(MEDIA_ID_CACHE_FILE, "utf-8").trim();
    }
  } catch (e) {
    // Ignore cache read errors
  }
  return null;
}

function saveCachedThumbMediaId(mediaId: string): void {
  try {
    const dir = path.dirname(MEDIA_ID_CACHE_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(MEDIA_ID_CACHE_FILE, mediaId);
  } catch (e) {
    // Ignore cache write errors
  }
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    console.log(`
Batch publish articles to WeChat Official Account draft using API

Usage:
  bun wechat-batch-api.ts <md-file1> [md-file2] ... [md-file8] [--cover <cover-url>]

Arguments:
  md-files            1-8 Markdown files to publish

Options:
  --cover <url>       Cover image URL (optional, used for all articles)
  --help              Show this help

Example:
  bun wechat-batch-api.ts article1.md article2.md --cover https://example.com/cover.jpg
  bun wechat-batch-api.ts article1.md article2.md  (uses default cover image)
`);
    process.exit(0);
  }
  
  // Parse arguments
  const mdFiles: string[] = [];
  let coverUrl = "";
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--cover" && args[i + 1]) {
      coverUrl = args[++i];
    } else if (!args[i].startsWith("--")) {
      mdFiles.push(args[i]);
    }
  }
  
  if (mdFiles.length === 0) {
    console.error("Error: At least one markdown file required");
    process.exit(1);
  }
  
  if (mdFiles.length > 8) {
    console.error("Error: Maximum 8 articles allowed");
    process.exit(1);
  }
  
  // Validate files exist
  for (const file of mdFiles) {
    const resolvedPath = path.resolve(file);
    if (!fs.existsSync(resolvedPath)) {
      console.error(`Error: File not found: ${file}`);
      process.exit(1);
    }
  }
  
  const config = loadConfig();
  console.error(`[wechat-batch-api] Fetching access token...`);
  const accessToken = await fetchAccessToken(config.appId, config.appSecret);
  
  console.error(`[wechat-batch-api] Processing ${mdFiles.length} articles...`);
  
  // Upload cover image once if provided, otherwise use cached or upload default
  let thumbMediaId: string;
  if (coverUrl) {
    console.error(`[wechat-batch-api] Uploading cover image...`);
    const coverResp = await uploadImage(coverUrl, accessToken);
    thumbMediaId = coverResp.media_id;
  } else {
    // Try to use cached media_id first
    const cachedMediaId = loadCachedThumbMediaId();
    if (cachedMediaId) {
      console.error(`[wechat-batch-api] Using cached cover image`);
      thumbMediaId = cachedMediaId;
    } else {
      console.error(`[wechat-batch-api] Uploading default cover image...`);
      const coverResp = await uploadImage(DEFAULT_COVER_URL, accessToken);
      thumbMediaId = coverResp.media_id;
      saveCachedThumbMediaId(thumbMediaId);
    }
  }
  
  const articles: ArticleData[] = [];
  
  for (const mdFile of mdFiles) {
    try {
      const article = await processArticle(path.resolve(mdFile), thumbMediaId, accessToken);
      articles.push(article);
    } catch (err) {
      console.error(`[wechat-batch-api] Failed to process ${mdFile}:`, err);
      process.exit(1);
    }
  }
  
  console.error(`[wechat-batch-api] Publishing ${articles.length} articles to draft...`);
  const mediaId = await publishDrafts(articles, accessToken);
  
  console.log(JSON.stringify({
    success: true,
    media_id: mediaId,
    article_count: articles.length,
    articles: articles.map(a => ({ title: a.title })),
  }, null, 2));
  
  console.error(`[wechat-batch-api] Published successfully! media_id: ${mediaId}`);
  console.error(`[wechat-batch-api] Articles:`);
  articles.forEach((a, i) => {
    console.error(`  ${i + 1}. ${a.title}`);
  });
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
