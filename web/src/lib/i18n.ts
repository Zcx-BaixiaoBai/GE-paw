// GE-paw Console i18n. Currently zh-CN only; the table is centralized
// so future locales can be added without touching every component.
export type Locale = "zh-CN";

export const dict = {
  // Brand
  "brand.name": "GE-paw",
  "brand.tagline": "浠ｇ悊绌洪棿 路 鏈湴杩愯",
  "favicon.title": "GE-paw 控制台",

  // Top bar
  "topbar.workspace": "宸ヤ綔鍖?,
  "topbar.newThread": "鏂板缓浼氳瘽",
  "topbar.untitledThread": "鏈懡鍚嶄細璇?,
  "topbar.toggleLeft": "鍒囨崲宸︿晶闈㈡澘 (Ctrl+B)",
  "topbar.toggleRight": "鍒囨崲鍙充晶闈㈡澘 (Ctrl+J)",
  "topbar.toggleTheme": "切换主题",
  "topbar.logout": "閫€鍑虹櫥褰?,
  "topbar.role.admin": "绠＄悊鍛?,
  "topbar.role.member": "鎴愬憳",
  "topbar.theme.dark": "娣辫壊涓婚",
  "topbar.theme.light": "娴呰壊涓婚",
  "topbar.theme.system": "璺熼殢绯荤粺",
  "topbar.menu.profile": "涓汉璧勬枡",
  "topbar.menu.settings": "璁剧疆",
  "topbar.menu.admin": "绠＄悊鍚庡彴",
  "topbar.menu.signout": "閫€鍑?,
  "topbar.rename": "閲嶅懡鍚嶄細璇?,
  "topbar.rename.placeholder": "浼氳瘽鏍囬",
  "topbar.archive": "褰掓。浼氳瘽",
  "topbar.unarchive": "鍙栨秷褰掓。",
  "topbar.pin": "鍥哄畾鍒伴《閮?,
  "topbar.unpin": "鍙栨秷鍥哄畾",

  // Left pane
  "left.newSession": "鏂板缓浼氳瘽",
  "left.section.modes": "妯″紡",
  "left.section.admin": "绠＄悊",
  "left.section.today": "浠婂ぉ",
  "left.section.week": "鏈懆",
  "left.section.month": "鏈湀",
  "left.section.earlier": "鏇存棭",
  "left.untitled": "鏈懡鍚嶄細璇?,
  "left.session.pin": "鍥哄畾鍒伴《閮?,
  "left.session.unpin": "鍙栨秷鍥哄畾",
  "left.session.rename": "閲嶅懡鍚?,
  "left.session.archive": "褰掓。",
  "left.session.unarchive": "鍙栨秷褰掓。",
  "left.session.delete": "鍒犻櫎浼氳瘽",
  "left.session.archived": "宸插綊妗?,
  "left.session.showArchived": "鏄剧ず宸插綊妗?,
  "left.session.confirmDelete": "纭鍒犻櫎浼氳瘽 \"{title}\"锛熸鎿嶄綔涓嶅彲鎾ら攢銆?,
  "left.mode.assistant": "鍔╂墜",
  "left.mode.qna": "鐭ヨ瘑闂瓟",
  "left.admin.llm": "LLM 鎺ュ彛",
  "left.admin.members": "鎴愬憳",
  "left.admin.channels": "閫氶亾",
  "left.admin.crons": "瀹氭椂浠诲姟",
  "left.admin.tokens": "Token 璁板綍",
  "left.admin.sessions": "浼氳瘽",
  "left.admin.wiki": "鐭ヨ瘑搴?,
  "left.admin.audit": "瀹¤鏃ュ織",
  "left.empty.threads": "灏氭棤浼氳瘽锛岀偣鍑讳笂鏂规柊寤轰竴涓惂",

  // Right pane tabs
  "tab.files": "文件",
  "tab.web": "网页",
  "tab.diff": "对比",
  "tab.preview": "预览",
  "tab.plan": "计划",
  "tab.goals": "目标",
  "tab.empty.title": "还没有可显示的标签页",
  "tab.empty.hint": "鍦ㄤ富鑱婂ぉ椤佃緭鍏?+ 鏂板缓鏍囩",
  "tab.menu.open": "鎵撳紑鏍囩椤?,
  "tab.menu.kbd.live": "鍙敤",
  "tab.menu.kbd.soon": "即将",
  "tab.none": "鏃犳爣绛鹃〉",
  "tab.files.hint": "工作区与知识库树",
  "tab.web.hint": "在外部网页中浏览 URL，便于审阅对话引用",
  "tab.diff.hint": "对比本会话中编辑过的文件改动",
  "tab.preview.hint": "多格式知识库预览",
  "tab.plan.hint": "助手生成的可验证计划步骤",
  "tab.goals.hint": "当前会话的可验证目标",

  // Plan tab / drawer
  "plan.session": "浼氳瘽",
  "plan.sessionPlaceholder": "浼氳瘽 ID",
  "plan.load": "鍔犺浇",
  "plan.loading": "鍔犺浇涓€?,
  "plan.empty.title": "尚未记录任何计划步骤",
  "plan.empty.hint": "开始一段新会话，助手会在合适时机提出可验证的计划步骤",
  "plan.tabHint": "在右侧选择会话并按加载查看该会话的已批准步骤",
  "plan.failed": "璁″垝鍔犺浇澶辫触",

  // Goals tab / drawer
  "goals.empty.title": "为该会话设定可验证目标",
  "goals.empty.hint": "助手会在合适时机把任务拆成可验证目标",
  "goals.status.pending": "寰呭姙",
  "goals.status.in_progress": "杩涜涓?,
  "goals.status.done": "宸插畬鎴?,
  "goals.status.failed": "澶辫触",
  "goals.status.label": "鐘舵€?,
  "goals.add": "娣诲姞鐩爣",
  "goals.addPlaceholder": "涓哄綋鍓嶄細璇濇坊鍔犱竴涓彲楠岃瘉鐩爣",
  "goals.delete": "鍒犻櫎",
  "goals.refresh": "鍒锋柊",
  "goals.loading": "鍔犺浇涓€?,
  "goals.tabHint": "为当前会话添加可验证目标，便于助手聚焦与回溯",
  "goals.count.short": "{done}/{total}",
  "goals.count.label": "已完成 {done} / 共 {total}",

  // Chat composer
  "chat.placeholder": "杈撳叆娑堟伅锛圕trl+Enter 鍙戦€侊級",
  "chat.send": "鍙戦€?,
  "chat.sending": "鍙戦€佷腑",
  "chat.stop": "鍋滄",
  "chat.regenerate": "閲嶆柊鐢熸垚",
  "chat.copy": "澶嶅埗",
  "chat.copied": "宸插鍒?,
  "chat.empty": "锛堢┖锛?,
  "chat.errorPrefix": "锛堝嚭閿欙級",
  "chat.noResponse": "锛堟棤鍝嶅簲锛?,
  "chat.tokensTip": "鏈浼氳瘽绱娑堣€?token",
  "chat.thinking.label": "正在思考",
  "chat.thinking.collapsed": "已思考 {seconds}s",
  "chat.thinking.toggle": "灞曞紑/鏀惰捣",
  "chat.tool.label": "宸ュ叿璋冪敤",
  "chat.tool.running": "运行中",
  "chat.tool.ok": "成功",
  "chat.tool.err": "失败",
    "chat.tool.result": "输出",
  "chat.tool.args": "参数",
  "chat.welcome.title": "娆㈣繋浣跨敤 GE-paw",
  "chat.welcome.sub": "浠ｇ悊绌洪棿 路 鏈湴杩愯",
  "chat.welcome.hint": "鎸?Ctrl+Enter 鍙戦€侊紝/ 鍞よ捣鍛戒护",
  "chat.permission.suffix": "鏉冮檺锛歿mode}",
  "chat.drawer.goals": "鐩爣",
  "chat.drawer.plan": "璁″垝",
  "chat.drawer.close": "鏀惰捣",
  "chat.model.label": "妯″瀷",
  "chat.permission.label": "鏉冮檺",

  // Permission menu
  "perm.full": "瀹屽叏璁块棶",
  "perm.full.desc": "鍙鍐欐枃浠跺苟鎵ц鍛戒护",
  "perm.smart": "鏅鸿兘鎵瑰噯",
  "perm.smart.desc": "甯歌鎿嶄綔鑷姩閫氳繃锛屾晱鎰熸搷浣滈渶纭",
  "perm.strict": "涓ユ牸瀹℃壒",
  "perm.strict.desc": "鎵€鏈夊啓鎿嶄綔閮介渶瑕佺‘璁?,
  "perm.readonly": "鍙",
  "perm.readonly.desc": "浠呭厑璁歌鍙栵紝涓嶅彲淇敼",
  "perm.changed": "鏉冮檺宸叉洿鏂?,

  // Theme menu
  "theme.menu.title": "涓婚",
  "theme.menu.light": "娴呰壊",
  "theme.menu.dark": "娣辫壊",
  "theme.menu.system": "璺熼殢绯荤粺",

  // QnA page
  "qna.badge": "鐭ヨ瘑搴?,
  "qna.placeholder": "鍩轰簬鐭ヨ瘑搴撴彁闂€?,
  "qna.ask": "鎻愰棶",
  "qna.asking": "妫€绱腑鈥?,
  "qna.empty.answer": "鏆傛棤绛旀",
  "qna.citations": "寮曠敤鏉ユ簮",
  "qna.recent": "杩戞湡闂",
  "qna.openInFiles": "鍦ㄥ彸渚ч潰鏉挎墦寮€",
  "qna.intro": "杈撳叆闂鍚庝粠鐭ヨ瘑搴撴绱㈢浉鍏崇瓟妗?,
    "qna.score": "鍒嗘暟 {score}",

  // Login page
  "login.title": "GE-paw",
  "login.subtitle": "鐧诲綍浠ョ户缁?,
  "login.username": "鐢ㄦ埛鍚?,
  "login.password": "瀵嗙爜",
  "login.submit": "鐧诲綍",
  "login.submitting": "鐧诲綍涓€?,
  "login.failed": "鐧诲綍澶辫触",

  // Modal (request user input)
  "modal.requestUserInput.title": "闇€瑕佹洿澶氫俊鎭?,
  "modal.requestUserInput.desc": "璇烽€夋嫨涓€涓€夐」锛屾垨杈撳叆鑷畾涔夊洖澶?,
  "modal.requestUserInput.other": "鑷畾涔?,
  "modal.requestUserInput.submit": "鎻愪氦",
  "modal.requestUserInput.cancel": "鍙栨秷",
  "modal.requestUserInput.placeholder": "璇疯緭鍏モ€?,

  // Errors
  "error.unknown": "鏈煡閿欒",

  // Admin - common
  "admin.common.add": "娣诲姞",
  "admin.common.delete": "鍒犻櫎",
  "admin.common.confirmDelete": "纭鍒犻櫎 {name}锛?,
  "admin.common.refresh": "鍒锋柊",
  "admin.common.save": "淇濆瓨",
  "admin.common.cancel": "鍙栨秷",
  "admin.common.loading": "鍔犺浇涓€?,
  "admin.common.empty": "鏆傛棤鏁版嵁",
  "admin.common.unknown": "鏈煡",

  // Admin - audit
  "admin.audit.title": "瀹¤鏃ュ織",
  "admin.audit.when": "鏃堕棿",
  "admin.audit.action": "鎿嶄綔",
  "admin.audit.target": "瀵硅薄",
  "admin.audit.actor": "鎿嶄綔鑰?,
  "admin.audit.empty": "鏆傛棤瀹¤璁板綍",

  // Admin - llm
  "admin.llm.title": "LLM 鎺ュ彛",
  "admin.llm.addTitle": "娣诲姞鎺ュ彛锛圤penAI 鍏煎锛?,
  "admin.llm.name": "鍚嶇О",
  "admin.llm.baseUrl": "Base URL",
  "admin.llm.apiKey": "API Key",
  "admin.llm.model": "妯″瀷",
  "admin.llm.maxTokens": "鏈€澶?Token",
  "admin.llm.temperature": "娓╁害",
  "admin.llm.isDefault": "榛樿",
  "admin.llm.enabled": "宸插惎鐢?,
  "admin.llm.list": "鐜版湁鎺ュ彛",
  "admin.llm.empty": "鏆傛棤 LLM 鎺ュ彛",

  // Admin - members
  "admin.members.title": "鎴愬憳",
  "admin.members.addTitle": "娣诲姞鐢ㄦ埛",
  "admin.members.username": "鐢ㄦ埛鍚?,
  "admin.members.display": "鏄电О",
  "admin.members.email": "閭",
  "admin.members.password": "瀵嗙爜",
  "admin.members.org": "缁勭粐",
  "admin.members.active": "宸叉縺娲?,
  "admin.members.empty": "鏆傛棤鐢ㄦ埛",

  // Admin - channels
  "admin.channels.title": "閫氶亾",
  "admin.channels.addTitle": "娣诲姞閫氶亾",
  "admin.channels.kind": "绫诲瀷",
  "admin.channels.name": "鍚嶇О",
  "admin.channels.credentials": "鍑嵁 (JSON)",
  "admin.channels.list": "鐜版湁閫氶亾",
  "admin.channels.reload": "閲嶈浇",
  "admin.channels.status": "鐘舵€?,
  "admin.channels.enabled": "宸插惎鐢?,
  "admin.channels.lastSeen": "鏈€鍚庢椿璺?,
  "admin.channels.listener": "鐩戝惉鍣?,
  "admin.channels.empty": "鏆傛棤閫氶亾",
  "admin.channels.running": "杩愯涓?,
    "admin.channels.runningCount": "杩愯涓細{count}",
    "admin.channels.hint": "鎻愮ず锛氫娇鐢?<code>echo</code> 绫诲瀷鍙€氳繃 <code>POST /api/webhook/echo</code> 杩涜杩涚▼鍐呮祴璇曘€?,
  "admin.channels.stopped": "鏈繍琛?,

  // Admin - crons
  "admin.crons.title": "瀹氭椂浠诲姟",
  "admin.crons.addTitle": "娣诲姞浠诲姟",
  "admin.crons.name": "鍚嶇О",
  "admin.crons.schedule": "璋冨害琛ㄨ揪寮?(cron)",
  "admin.crons.prompt": "鎻愮ず璇嶆ā鏉?,
  "admin.crons.lastStatus": "涓婃鐘舵€?,
  "admin.crons.lastRun": "涓婃杩愯",
  "admin.crons.nextRun": "涓嬫杩愯",
  "admin.crons.failures": "杩炵画澶辫触",
    "admin.crons.enable": "鍚敤",
    "admin.crons.disable": "绂佺敤",
    "admin.crons.hint": "杈撳嚭浼氳褰曞埌 cron_run 骞惰鍏?token_usage_log銆傝繛缁?3 娆″け璐ヤ細鑷姩绂佺敤浠诲姟銆?,
  "admin.crons.empty": "鏆傛棤瀹氭椂浠诲姟",

  // Admin - tokens
  "admin.tokens.title": "Token 鐢ㄩ噺",
  "admin.tokens.window": "绐楀彛",
  "admin.tokens.last24h": "鏈€杩?24 灏忔椂",
  "admin.tokens.last7d": "鏈€杩?7 澶?,
  "admin.tokens.last30d": "鏈€杩?30 澶?,
  "admin.tokens.last90d": "鏈€杩?90 澶?,
  "admin.tokens.byModel": "鎸夋ā鍨?,
  "admin.tokens.byDay": "鎸夋棩",
  "admin.tokens.byUser": "鎸夌敤鎴?,
  "admin.tokens.calls": "璋冪敤娆℃暟",
  "admin.tokens.prompt": "杈撳叆 Token",
  "admin.tokens.completion": "杈撳嚭 Token",
  "admin.tokens.total": "鎬?Token",
  "admin.tokens.cost": "璐圭敤 (鍒?",
    "admin.tokens.summary": "鎬昏 {calls} 娆¤皟鐢?/ {tokens} tokens / {cents} 鍒?,
    "admin.tokens.emptyWindow": "褰撳墠绐楀彛鏆傛棤鏁版嵁銆?,
    "admin.tokens.knownHint": "宸茬煡榛樿浠锋牸锛歿models}",
  "admin.tokens.empty": "鏆傛棤鐢ㄩ噺",
  "admin.tokens.monthToDate": "鏈湀绱",
  "admin.tokens.costTable": "璐圭敤琛?,

  // Admin - sessions
  "admin.sessions.title": "浼氳瘽",
  "admin.sessions.allChannels": "鍏ㄩ儴閫氶亾",
  "admin.sessions.title2": "鏍囬",
  "admin.sessions.user": "鐢ㄦ埛",
  "admin.sessions.channel": "閫氶亾",
  "admin.sessions.messages": "娑堟伅鏁?,
  "admin.sessions.status": "鐘舵€?,
  "admin.sessions.lastActivity": "鏈€鍚庢椿璺?,
  "admin.sessions.empty": "鏆傛棤浼氳瘽",
  "admin.sessions.archived": "宸插綊妗?,
  "admin.sessions.web": "缃戦〉",
  "admin.sessions.archive": "褰掓。",
  "admin.sessions.delete": "鍒犻櫎",

  // Admin - wiki
  "admin.wiki.title": "鐭ヨ瘑搴擄紙鏈嶅姟绔鏂欙級",
  "admin.wiki.upload": "涓婁紶",
  "admin.wiki.triggerIngest": "瑙﹀彂瀵煎叆",
  "admin.wiki.compileIndex": "鏋勫缓绱㈠紩",
  "admin.wiki.resetAll": "娓呯┖鍏ㄩ儴",
  "admin.wiki.path": "璺緞",
  "admin.wiki.status": "鐘舵€?,
  "admin.wiki.size": "澶у皬",
  "admin.wiki.error": "閿欒",
  "admin.wiki.empty": "鏆傛棤涓婁紶",
  "admin.wiki.log": "鏃ュ織",
  "admin.wiki.uploadHint": "鏀寔 txt / md / pdf / docx 涓婁紶鍚庣敱鏈嶅姟绔В鏋愬拰宓屽叆",
  "admin.wiki.confirmReset": "纭畾娓呯┖鍏ㄩ儴鐭ヨ瘑搴撴簮涓庨〉闈㈠悧锛?,
  "admin.wiki.logUploaded": "宸蹭笂浼狅細{path}",
  "admin.wiki.logUploadFailed": "涓婁紶澶辫触锛歿err}",
  "admin.wiki.logIngest": "瀵煎叆锛歿result}",
  "admin.wiki.logIngestFailed": "瀵煎叆澶辫触锛歿err}",
  "admin.wiki.logCompile": "鏋勫缓绱㈠紩锛歿result}",
  "admin.wiki.logCompileFailed": "鏋勫缓绱㈠紩澶辫触锛歿err}",
  "admin.wiki.logReset": "宸叉竻绌?,
  "admin.wiki.logResetFailed": "娓呯┖澶辫触锛歿err}",

  // Common UI
  "common.dash": "鈥?,
  "common.dots": "鈥?,

} as const;

export type Key = keyof typeof dict;

export function t(key: Key, vars?: Record<string, string | number>): string {
  let s = (dict as any)[key] ?? key;
  if (vars) for (const [k, v] of Object.entries(vars)) s = s.split("{" + k + "}").join(String(v));
  return s;
}












