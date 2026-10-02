const { chromium } = require("playwright");
const out = "/Users/owenwassmer/dev/handoff-ferro/fe/nav";
require("fs").mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const results = [], errors = [];
  const check = (name, ok, detail = "") => results.push(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  (" + detail + ")" : ""}`);
  for (const [w, h] of [[1440, 900], [1024, 768], [390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    p.on("pageerror", (e) => errors.push(`${w} ${e}`)); p.on("console", (m) => m.type() === "error" && errors.push(`${w} ${m.text()}`));
    await p.goto("http://localhost:5199/preview.html?state=live"); await p.click(".unit-name a"); await p.waitForSelector(".unit-head"); await p.waitForTimeout(400);
    const tab = async (t) => { await p.click(`.unit-tabs button:has-text("${t}")`); await p.waitForTimeout(400); };
    const state = (sels) => p.evaluate((s) => ({ win: window.scrollY, page: document.documentElement.scrollHeight - innerHeight,
      panes: Object.fromEntries(s.map((x) => [x, document.querySelector(x)?.scrollTop ?? null])) }), sels);
    const wheelOver = async (sel, sels) => {
      await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(100);
      const box = await p.locator(sel).first().boundingBox(); if (!box) return null;
      const before = await state(sels);
      await p.mouse.move(box.x + box.width / 2, box.y + Math.min(box.height / 2, 200)); await p.mouse.wheel(0, 600); await p.waitForTimeout(350);
      return { before, after: await state(sels) };
    };
    const split = w > 720;
    // Any element that scrolls by only a few pixels shows a scrollbar for nothing.
    const stray = () => p.evaluate(() => [...document.querySelectorAll("body *")].filter((el) => {
      const cs = getComputedStyle(el); if (el.clientHeight === 0 && el.clientWidth === 0) return false;
      const y = /auto|scroll/.test(cs.overflowY) && el.scrollHeight - el.clientHeight > 0 && el.scrollHeight - el.clientHeight <= 4;
      const x = /auto|scroll/.test(cs.overflowX) && el.scrollWidth - el.clientWidth > 0 && el.scrollWidth - el.clientWidth <= 4;
      return y || x;
    }).map((el) => `${el.tagName.toLowerCase()}.${[...el.classList].join(".")}`));
    const pageHeights = {};
    // Documents: list and open document scroll independently; the page does not.
    await tab("Documents");
    await p.locator(".doc-item").nth(3).click(); await p.waitForTimeout(400);
    const dsel = [".doc-list", ".doc-pane"];
    pageHeights.documents = await p.evaluate(() => document.documentElement.scrollHeight);
    check(`${w} Documents: no stray scrollbars`, (await stray()).length === 0, JSON.stringify(await stray()));
    check(`${w} Documents: tab keeps its natural height`, await p.evaluate(() => document.querySelector(".tab-panel").style.height === ""));
    await p.evaluate(() => { const l = document.querySelector(".doc-list"); l.innerHTML += '<div style="height:1600px" data-probe></div>'; });
    let r = await wheelOver(".doc-list", dsel);
    if (split) {
      check(`${w} Documents: wheel over the list scrolls the list`, r.after.panes[".doc-list"] > 0 && r.after.win === 0, JSON.stringify(r.after));
      check(`${w} Documents: open document stays put`, r.after.panes[".doc-pane"] === r.before.panes[".doc-pane"]);
      await p.evaluate(() => { const d = document.querySelector(".doc-pane"); d.innerHTML += '<div style="height:1600px" data-probe></div>'; });
      r = await wheelOver(".doc-pane", dsel);
      check(`${w} Documents: wheel over the document scrolls the document`, r.after.panes[".doc-pane"] > 0 && r.after.win === 0, JSON.stringify(r.after));
      check(`${w} Documents: list stays put`, r.after.panes[".doc-list"] === r.before.panes[".doc-list"]);
    } else {
      check(`${w} Documents: single column scrolls the page`, r.after.win > 0, JSON.stringify(r.after));
    }
    await p.screenshot({ path: `${out}/documents-${w}.png` });
    // Messages
    await tab("Messages");
    const msel = [".inbox", ".thread-pane"];
    pageHeights.messages = await p.evaluate(() => document.documentElement.scrollHeight);
    check(`${w} Messages: no stray scrollbars`, (await stray()).length === 0, JSON.stringify(await stray()));
    await p.evaluate(() => { const t = document.querySelector(".thread-pane"); if (t) t.innerHTML += '<div style="height:1600px" data-probe></div>'; const l = document.querySelector(".inbox"); if (l) l.innerHTML += '<li style="height:1600px"></li>'; });
    if (split) {
      r = await wheelOver(".inbox", msel);
      check(`${w} Messages: wheel over conversations scrolls them only`, r.after.panes[".inbox"] > 0 && r.after.panes[".thread-pane"] === 0 && r.after.win === 0, JSON.stringify(r.after));
      r = await wheelOver(".thread-pane", msel);
      check(`${w} Messages: wheel over the thread scrolls it only`, r.after.panes[".thread-pane"] > 0 && r.after.panes[".inbox"] === r.before.panes[".inbox"] && r.after.win === 0, JSON.stringify(r.after));
    }
    if (split) {
      await p.goto("http://localhost:5199/preview.html?state=live"); await p.click(".unit-name a"); await p.waitForSelector(".unit-head"); await p.waitForTimeout(300); await tab("Documents");
      await p.locator(".doc-item").nth(3).click(); await p.waitForTimeout(400);
      const room = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
      // Scroll the list to its end first; the next wheel over it must carry on to the page.
      await p.evaluate(() => window.scrollTo(0, 0));
      await p.evaluate(() => { const l = document.querySelector(".doc-list"); l.scrollTop = l.scrollHeight; }); await p.waitForTimeout(150);
      const lb = await p.locator(".doc-list").boundingBox();
      await p.mouse.move(lb.x + lb.width / 2, lb.y + Math.min(lb.height / 2, 200)); await p.mouse.wheel(0, 400); await p.waitForTimeout(350);
      r = { after: await state(dsel) };
      if (room > 0) check(`${w} Documents: at a pane's end the page scrolls on`, r.after.win > 0, JSON.stringify(r.after));
      await tab("Messages");
    }
    await p.screenshot({ path: `${out}/messages-${w}.png` });
    // Money: each quote lists its lines; the section toggle folds and unfolds them.
    await tab("Money");
    const q = 'section[aria-labelledby="quotes-title"]';
    check(`${w} Money: quote lines start folded`, (await p.locator(`${q} tr.line-row`).count()) === 0);
    await p.locator(`${q} button:has-text("Expand all")`).click(); await p.waitForTimeout(150);
    const linesOpen = await p.locator(`${q} tr.line-row`).count();
    check(`${w} Money: Expand all shows the lines`, linesOpen > 0, `${linesOpen} lines`);
    // No cell but a description wraps in the document tables.
    const wrapped = await p.evaluate(() => [...document.querySelectorAll(".rows.docs tbody tr:not(.line-row) td:not(:nth-child(2))")]
      .filter((td) => { if (!td.offsetParent) return false;
        const walk = document.createTreeWalker(td, NodeFilter.SHOW_TEXT); let n, wraps = false;
        while ((n = walk.nextNode())) { if (!n.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(n);
          if (new Set([...r.getClientRects()].filter((x) => x.width > 1).map((x) => Math.round(x.top))).size > 1) wraps = true; }
        return wraps; })
      .map((td) => td.innerText.slice(0, 30)));
    check(`${w} Money: names, dates, statuses and amounts stay on one line`, w <= 720 || wrapped.length === 0, JSON.stringify(wrapped));
    await p.locator(`${q} button.disclose`).first().click(); await p.waitForTimeout(150);
    check(`${w} Money: one row folds on its own`, (await p.locator(`${q} tr.line-row`).count()) < linesOpen);
    await p.locator(`${q} button.disclose`).first().click(); await p.waitForTimeout(150);
    // Money: drawer is the only thing that scrolls; Escape closes it and focus returns to the page.
    await tab("Money");
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.screenshot({ path: `${out}/money-${w}.png`, fullPage: true });
    await p.locator('section[aria-labelledby="invoices-title"] button.link').first().click(); await p.waitForSelector(".drawer");
    await p.waitForTimeout(300);
    check(`${w} Money: drawer takes focus`, await p.evaluate(() => document.activeElement?.classList.contains("drawer")));
    await p.screenshot({ path: `${out}/money-drawer-${w}.png` });
    await p.evaluate(() => { document.querySelector(".drawer").innerHTML += '<div style="height:1600px"></div>'; });
    r = await wheelOver(".drawer", [".drawer"]);
    check(`${w} Money: wheel over the drawer scrolls the drawer, not the page`, r.after.panes[".drawer"] > 0 && r.after.win === 0, JSON.stringify(r.after));
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    check(`${w} Money: Escape closes the drawer and unlocks the page`, (await p.locator(".drawer").count()) === 0 && (await p.evaluate(() => document.body.style.overflow)) === "");
    await tab("Calendar");
    const heads = await p.locator(".month-head").allInnerTexts();
    check(`${w} Calendar: week runs Sunday to Saturday`, heads[0].toLowerCase() === "sun" && heads[6].toLowerCase() === "sat", heads.join(" "));
    const firstCell = await p.evaluate(() => { const c = document.querySelector(".month-cell"); return c?.getAttribute("data-weekend"); });
    check(`${w} Calendar: first column is a weekend day`, firstCell === "true");
    for (const t of ["Money", "Timeline", "Calendar", "Overview"]) {
      await tab(t); const s = await stray();
      check(`${w} ${t}: no stray scrollbars`, s.length === 0, JSON.stringify(s));
    }
    // Overview: ordinary page scroll; funds line opens Money.
    await tab("Overview");
    r = await wheelOver(".main-col", []);
    check(`${w} Overview: long page scrolls normally`, r.after.win > 0, `scrollY ${r.after.win}`);
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.click("text=Open Money"); await p.waitForTimeout(300);
    check(`${w} Overview: Open Money goes to the Money tab`, (await p.locator('.unit-tabs button[aria-selected="true"]').innerText()).startsWith("Money"));
    // Tabs are reachable by keyboard.
    await p.locator('.unit-tabs button:has-text("Timeline")').focus(); await p.keyboard.press("Enter"); await p.waitForTimeout(300);
    check(`${w} Keyboard: Enter on a tab opens it`, (await p.locator('.unit-tabs button[aria-selected="true"]').innerText()).startsWith("Timeline"));
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    check(`${w} No horizontal overflow`, sw <= w, `${sw}`);
    results.push(`INFO  ${w} page heights ${JSON.stringify(pageHeights)} viewport ${h}`);
    await p.close();
  }
  await b.close();
  console.log(results.join("\n")); console.log("errors:", JSON.stringify(errors));
})().catch((e) => { console.error(e); process.exit(1); });
