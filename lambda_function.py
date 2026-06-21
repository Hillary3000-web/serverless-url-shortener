<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Cirrus — short links, served serverless</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
<style>
  :root{
    --ink:#0A0E1A;
    --ink-2:#0E1424;
    --glass:rgba(255,255,255,.045);
    --glass-2:rgba(255,255,255,.07);
    --line:rgba(255,255,255,.10);
    --text:#EAEEFB;
    --muted:#8893B0;
    --blue:#5B8CFF;
    --blue-deep:#3a5bd9;
    --amber:#FFB454;
    --amber-deep:#F59E2C;
    --good:#5BE3B3;
    --bad:#FF7A8A;
    --display:'Space Grotesk',system-ui,sans-serif;
    --mono:'JetBrains Mono',ui-monospace,monospace;
  }

  *{box-sizing:border-box;margin:0;padding:0}

  html,body{height:100%}

  body{
    font-family:var(--display);
    background:var(--ink);
    color:var(--text);
    min-height:100dvh;
    display:flex;
    flex-direction:column;
    overflow-x:hidden;
    -webkit-font-smoothing:antialiased;
    position:relative;
  }

  /* ambient cloud atmosphere */
  .atmos{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}
  .blob{position:absolute;border-radius:50%;filter:blur(80px);opacity:.5;animation:drift 22s ease-in-out infinite}
  .blob.b1{width:520px;height:520px;background:radial-gradient(circle,#2c46a8,transparent 70%);top:-160px;left:-120px}
  .blob.b2{width:480px;height:480px;background:radial-gradient(circle,#6b3fa0,transparent 70%);bottom:-180px;right:-100px;animation-delay:-7s}
  .blob.b3{width:360px;height:360px;background:radial-gradient(circle,#b9772a,transparent 70%);bottom:10%;left:30%;opacity:.28;animation-delay:-13s}
  @keyframes drift{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(40px,-30px) scale(1.08)}66%{transform:translate(-30px,20px) scale(.96)}}

  .grain{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.035;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}

  /* layout */
  header,main,footer{position:relative;z-index:2}

  header{
    display:flex;align-items:center;justify-content:space-between;
    padding:26px clamp(20px,5vw,56px);
  }
  .wordmark{display:flex;align-items:center;gap:10px;font-weight:700;font-size:19px;letter-spacing:-.01em}
  .mark{width:26px;height:26px;display:grid;place-items:center;border-radius:8px;
    background:linear-gradient(135deg,var(--blue),var(--blue-deep));box-shadow:0 4px 16px rgba(91,140,255,.4)}
  .mark svg{width:15px;height:15px}
  .nav-tag{font-family:var(--mono);font-size:11.5px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase}

  main{
    flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:clamp(28px,6vh,72px) clamp(20px,5vw,40px);
    width:100%;
  }

  .stage{width:100%;max-width:640px;text-align:center}

  .eyebrow{
    font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--amber);margin-bottom:18px;display:inline-flex;align-items:center;gap:8px;
  }
  .eyebrow::before{content:"";width:18px;height:1px;background:var(--amber);opacity:.6}
  .eyebrow::after{content:"";width:18px;height:1px;background:var(--amber);opacity:.6}

  h1{
    font-size:clamp(34px,6.4vw,60px);line-height:1.02;letter-spacing:-.03em;font-weight:600;
    margin-bottom:18px;
  }
  h1 .out{color:var(--blue)}

  .sub{color:var(--muted);font-size:clamp(15px,2.2vw,17px);line-height:1.55;max-width:440px;margin:0 auto 40px}

  /* input card */
  .card{
    background:var(--glass);border:1px solid var(--line);border-radius:18px;
    padding:10px;display:flex;gap:8px;align-items:center;
    box-shadow:0 24px 60px -24px rgba(0,0,0,.7), inset 0 1px 0 rgba(255,255,255,.05);
    transition:border-color .25s, box-shadow .25s;
  }
  .card:focus-within{border-color:rgba(91,140,255,.55);box-shadow:0 24px 60px -24px rgba(0,0,0,.7),0 0 0 4px rgba(91,140,255,.14)}

  .card input{
    flex:1;background:transparent;border:0;outline:0;color:var(--text);
    font-family:var(--mono);font-size:15px;padding:14px 16px;min-width:0;
  }
  .card input::placeholder{color:rgba(136,147,176,.65)}

  button{font-family:var(--display);cursor:pointer;border:0;font-weight:600}

  .go{
    background:linear-gradient(135deg,var(--amber),var(--amber-deep));
    color:#2a1605;font-size:15px;padding:14px 22px;border-radius:12px;white-space:nowrap;
    display:inline-flex;align-items:center;gap:8px;letter-spacing:-.01em;
    box-shadow:0 8px 20px -6px rgba(245,158,44,.5);transition:transform .15s, box-shadow .15s, opacity .2s;
  }
  .go:hover{transform:translateY(-1px);box-shadow:0 12px 26px -6px rgba(245,158,44,.6)}
  .go:active{transform:translateY(0)}
  .go:disabled{opacity:.55;cursor:default;transform:none;box-shadow:none}
  .go .spin{width:15px;height:15px;border:2px solid rgba(42,22,5,.35);border-top-color:#2a1605;border-radius:50%;animation:rot .6s linear infinite;display:none}
  @keyframes rot{to{transform:rotate(360deg)}}
  body.loading .go .label{display:none}
  body.loading .go .spin{display:inline-block}

  .hint{margin-top:14px;font-family:var(--mono);font-size:12px;color:var(--muted);min-height:16px;text-align:left;padding-left:6px;transition:color .2s}
  .hint.err{color:var(--bad)}

  /* result */
  .result{margin-top:30px;opacity:0;transform:translateY(14px);pointer-events:none;transition:opacity .5s, transform .5s}
  .result.show{opacity:1;transform:none;pointer-events:auto}

  .compress{
    display:flex;align-items:center;justify-content:center;gap:14px;
    font-family:var(--mono);font-size:13px;color:var(--muted);margin-bottom:18px;
  }
  .compress b{color:var(--good);font-weight:700}
  .compress .arrow{color:var(--blue)}

  .out-card{
    background:linear-gradient(180deg,var(--glass-2),var(--glass));
    border:1px solid var(--line);border-radius:16px;padding:20px;
    display:flex;align-items:center;gap:14px;flex-wrap:wrap;
  }
  .out-link{
    flex:1;min-width:200px;text-align:left;font-family:var(--mono);font-size:15px;
    color:var(--blue);text-decoration:none;word-break:break-all;font-weight:500;
  }
  .out-link:hover{text-decoration:underline}

  .acts{display:flex;gap:8px}
  .ghost{
    background:var(--glass-2);color:var(--text);border:1px solid var(--line);
    padding:11px 16px;border-radius:10px;font-size:13.5px;display:inline-flex;align-items:center;gap:7px;
    transition:background .2s,border-color .2s,color .2s;
  }
  .ghost:hover{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.2)}
  .ghost.copied{color:var(--good);border-color:rgba(91,227,179,.4)}
  .ghost svg{width:14px;height:14px}

  footer{
    padding:22px clamp(20px,5vw,56px);
    display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;
    font-size:12.5px;color:var(--muted);border-top:1px solid rgba(255,255,255,.06);
  }
  .stack{font-family:var(--mono);font-size:11.5px;letter-spacing:.02em}
  .stack span{color:#aeb8d4}
  footer a{color:var(--muted);text-decoration:none}
  footer a:hover{color:var(--text)}

  @media (max-width:540px){
    .card{flex-direction:column;align-items:stretch;gap:6px}
    .go{justify-content:center;padding:15px}
    .acts{width:100%}
    .ghost{flex:1;justify-content:center}
    .nav-tag{display:none}
  }

  @media (prefers-reduced-motion:reduce){
    .blob{animation:none}
    *{transition-duration:.01ms!important}
  }
</style>
</head>
<body>
  <div class="atmos"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>
  <div class="grain"></div>

  <header>
    <div class="wordmark">
      <span class="mark">
        <svg viewBox="0 0 24 24" fill="none"><path d="M9 15a4 4 0 0 1 0-6l2-2a4 4 0 0 1 6 6l-1 1" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/><path d="M15 9a4 4 0 0 1 0 6l-2 2a4 4 0 0 1-6-6l1-1" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>
      </span>
      Cirrus
    </div>
    <span class="nav-tag">serverless · aws</span>
  </header>

  <main>
    <div class="stage">
      <span class="eyebrow">link shortener</span>
      <h1>Long URL in.<br><span class="out">Short link out.</span></h1>
      <p class="sub">Paste a long, unwieldy link and get a short one you can share anywhere — created in milliseconds by a serverless backend.</p>

      <div class="card">
        <input id="url" type="url" inputmode="url" autocomplete="off" spellcheck="false"
               placeholder="https://your-very-long-link.com/goes/right/here" />
        <button class="go" id="go">
          <span class="label">Shorten link</span>
          <span class="spin"></span>
        </button>
      </div>
      <div class="hint" id="hint">Press enter or hit shorten to compress your link.</div>

      <div class="result" id="result">
        <div class="compress" id="compress"></div>
        <div class="out-card">
          <a class="out-link" id="outLink" href="#" target="_blank" rel="noopener"></a>
          <div class="acts">
            <button class="ghost" id="copy">
              <svg viewBox="0 0 24 24" fill="none"><rect x="9" y="9" width="11" height="11" rx="2" stroke="currentColor" stroke-width="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10" stroke="currentColor" stroke-width="2"/></svg>
              <span>Copy</span>
            </button>
            <button class="ghost" id="open">
              <svg viewBox="0 0 24 24" fill="none"><path d="M7 17 17 7M17 7H9m8 0v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>Open</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer>
    <div class="stack">Powered by <span>AWS Lambda</span> · <span>API Gateway</span> · <span>DynamoDB</span></div>
    <div>Built by Hillary Chukwuma · <a href="https://github.com/Hillary3000-web" target="_blank" rel="noopener">github.com/Hillary3000-web</a></div>
  </footer>

<script>
  // ── Your API endpoint ───────────────────────────────────────────
  const API = "https://uqoal9nz9j.execute-api.us-east-1.amazonaws.com/shorten";

  const $ = s => document.querySelector(s);
  const input = $("#url"), go = $("#go"), hint = $("#hint");
  const result = $("#result"), outLink = $("#outLink"), compress = $("#compress");
  const copyBtn = $("#copy"), openBtn = $("#open");

  function setHint(msg, isErr=false){ hint.textContent = msg; hint.classList.toggle("err", isErr); }

  function normalize(u){
    u = u.trim();
    if(!u) return u;
    if(!/^https?:\/\//i.test(u)) u = "https://" + u;
    return u;
  }

  // animate the character-count compression
  function animateCompress(fromLen, toLen){
    compress.innerHTML = `<span id="cn">${fromLen}</span>&nbsp;<span class="arrow">→</span>&nbsp;<b id="ct">${fromLen}</b>&nbsp;characters`;
    const ct = $("#ct");
    const start = performance.now(), dur = 650;
    function step(now){
      const p = Math.min((now-start)/dur, 1);
      const eased = 1-Math.pow(1-p,3);
      ct.textContent = Math.round(fromLen + (toLen-fromLen)*eased);
      if(p<1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  async function shorten(){
    const raw = input.value;
    const url = normalize(raw);
    if(!url){ setHint("Paste a link first — anything starting with http works.", true); input.focus(); return; }

    document.body.classList.add("loading");
    go.disabled = true;
    setHint("Compressing…");

    try{
      const res = await fetch(API, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ url })
      });

      if(!res.ok){
        const txt = await res.text().catch(()=> "");
        throw new Error(`Server returned ${res.status}. ${txt}`);
      }

      const data = await res.json();
      const short = data.short_url;

      outLink.textContent = short;
      outLink.href = short;
      animateCompress(url.length, (data.code || "").length || 6);
      result.classList.add("show");
      setHint("Done. Your short link is ready to share.");
      copyBtn.querySelector("span").textContent = "Copy";
      copyBtn.classList.remove("copied");

    }catch(err){
      result.classList.remove("show");
      if(err.message && err.message.includes("Failed to fetch")){
        setHint("Couldn't reach the API — if you just deployed, check that CORS is enabled on API Gateway.", true);
      }else{
        setHint(err.message || "Something went wrong. Try again.", true);
      }
    }finally{
      document.body.classList.remove("loading");
      go.disabled = false;
    }
  }

  go.addEventListener("click", shorten);
  input.addEventListener("keydown", e => { if(e.key==="Enter") shorten(); });

  copyBtn.addEventListener("click", async () => {
    try{
      await navigator.clipboard.writeText(outLink.textContent);
      copyBtn.classList.add("copied");
      copyBtn.querySelector("span").textContent = "Copied";
      setTimeout(()=>{ copyBtn.classList.remove("copied"); copyBtn.querySelector("span").textContent="Copy"; }, 1800);
    }catch{ setHint("Copy failed — select the link and copy manually.", true); }
  });

  openBtn.addEventListener("click", () => {
    const u = outLink.href;
    if(u && u !== "#") window.open(u, "_blank", "noopener");
  });
</script>
</body>
</html>
