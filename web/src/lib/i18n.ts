// GE-paw Console i18n. Currently zh-CN only; the table is centralized
// so future locales can be added without touching every component.
export type Locale = "zh-CN";

export const dict = {
  // Brand
  "brand.name": "GE-paw",
  "brand.tagline": "代理空间 · 本地运行",
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
  "topbar.rename": "重命名会话",
  "topbar.rename.placeholder": "会话标题",
  "topbar.archive": "归档会话",
  "topbar.unarchive": "取消归档",
  "topbar.pin": "固定到顶部",
  "topbar.unpin": "取消固定",

  // Left pane
  "left.newSession": "新建会话",
  "left.section.modes": "妯″紡",
  "left.section.admin": "管理",
  "left.section.today": "今天",
  "left.section.week": "本周",
  "left.section.month": "本月",
  "left.section.earlier": "更早",
  "left.untitled": "未命名会话",
  "left.session.pin": "固定到顶部",
  "left.session.unpin": "取消固定",
  "left.session.rename": "重命名",
  "left.session.archive": "归档",
  "left.session.unarchive": "取消归档",
  "left.session.delete": "删除会话",
  "left.session.archived": "已归档",
  "left.session.showArchived": "显示已归档",
  "left.session.confirmDelete": "确认删除会话 \"{title}\"？此操作不可撤销。",
  "left.mode.assistant": "助手",
  "left.mode.qna": "知识问答",
  "left.admin.llm": "LLM 接口",
  "left.admin.members": "成员",
  "left.admin.channels": "通道",
  "left.admin.crons": "定时任务",
  "left.admin.tokens": "Token 记录",
  "left.admin.sessions": "会话",
  "left.admin.wiki": "知识库",
  "left.admin.audit": "审计日志",
  "left.empty.threads": "尚无会话，点击上方新建一个吧",

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
  "tab.menu.kbd.live": "可用",
  "tab.menu.kbd.soon": "即将",
  "tab.none": "鏃犳爣绛鹃〉",
  "tab.files.hint": "工作区与知识库树",
  "tab.web.hint": "在外部网页中浏览 URL，便于审阅对话引用",
  "tab.diff.hint": "对比本会话中编辑过的文件改动",
  "tab.preview.hint": "多格式知识库预览",
  "tab.plan.hint": "助手生成的可验证计划步骤",
  "tab.goals.hint": "当前会话的可验证目标",

  // Plan tab / drawer
  "plan.session": "会话",
  "plan.sessionPlaceholder": "会话 ID",
  "plan.load": "鍔犺浇",
  "plan.loading": "加载中…",
  "plan.empty.title": "尚未记录任何计划步骤",
  "plan.empty.hint": "开始一段新会话，助手会在合适时机提出可验证的计划步骤",
  "plan.tabHint": "在右侧选择会话并按加载查看该会话的已批准步骤",
  "plan.failed": "计划加载失败",

  // Goals tab / drawer
  "goals.empty.title": "为该会话设定可验证目标",
  "goals.empty.hint": "助手会在合适时机把任务拆成可验证目标",
  "goals.status.pending": "待办",
  "goals.status.in_progress": "进行中",
  "goals.status.done": "已完成",
  "goals.status.failed": "失败",
  "goals.status.label": "鐘舵€?,
  "goals.add": "添加目标",
  "goals.addPlaceholder": "为当前会话添加一个可验证目标",
  "goals.delete": "删除",
  "goals.refresh": "刷新",
  "goals.loading": "鍔犺浇涓€?,
  "goals.tabHint": "为当前会话添加可验证目标，便于助手聚焦与回溯",
  "goals.count.short": "{done}/{total}",
  "goals.count.label": "已完成 {done} / 共 {total}",

  // Chat composer
  "chat.placeholder": "输入消息（Ctrl+Enter 发送）",
  "chat.send": "发送",
  "chat.sending": "发送中",
  "chat.stop": "停止",
  "chat.regenerate": "閲嶆柊鐢熸垚",
  "chat.copy": "澶嶅埗",
  "chat.copied": "宸插鍒?,
  "chat.empty": "锛堢┖锛?,
  "chat.errorPrefix": "（出错）",
  "chat.noResponse": "（无响应）",
  "chat.tokensTip": "本次会话累计消耗 token",
  "chat.thinking.label": "正在思考",
  "chat.thinking.collapsed": "已思考 {seconds}s",
  "chat.thinking.toggle": "灞曞紑/鏀惰捣",
  "chat.tool.label": "宸ュ叿璋冪敤",
  "chat.tool.running": "运行中",
  "chat.tool.ok": "成功",
  "chat.tool.err": "失败",
    "chat.tool.result": "输出",
  "chat.tool.args": "参数",
  "chat.welcome.title": "欢迎使用 GE-paw",
  "chat.welcome.sub": "代理空间 · 本地运行",
  "chat.welcome.hint": "按 Ctrl+Enter 发送，/ 唤起命令",
  "chat.permission.suffix": "鏉冮檺锛歿mode}",
  "chat.drawer.goals": "目标",
  "chat.drawer.plan": "计划",
  "chat.drawer.close": "收起",
  "chat.model.label": "妯″瀷",
  "chat.permission.label": "鏉冮檺",

  // Permission menu
  "perm.full": "完全访问",
  "perm.full.desc": "可读写文件并执行命令",
  "perm.smart": "智能批准",
  "perm.smart.desc": "常规操作自动通过，敏感操作需确认",
  "perm.strict": "严格审批",
  "perm.strict.desc": "所有写操作都需要确认",
  "perm.readonly": "只读",
  "perm.readonly.desc": "仅允许读取，不可修改",
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
  "modal.requestUserInput.title": "需要更多信息",
  "modal.requestUserInput.desc": "请选择一个选项，或输入自定义回复",
  "modal.requestUserInput.other": "自定义",
  "modal.requestUserInput.submit": "提交",
  "modal.requestUserInput.cancel": "取消",
  "modal.requestUserInput.placeholder": "请输入…",

  // Errors
  "error.unknown": "未知错误",

  // Admin - common
  "admin.common.add": "添加",
  "admin.common.delete": "删除",
  "admin.common.confirmDelete": "确认删除 {name}？",
  "admin.common.refresh": "刷新",
  "admin.common.save": "保存",
  "admin.common.cancel": "取消",
  "admin.common.loading": "加载中…",
  "admin.common.empty": "暂无数据",
  "admin.common.unknown": "未知",

  // Admin - audit
  "admin.audit.title": "瀹¤鏃ュ織",
  "admin.audit.when": "鏃堕棿",
  "admin.audit.action": "鎿嶄綔",
  "admin.audit.target": "瀵硅薄",
  "admin.audit.actor": "鎿嶄綔鑰?,
  "admin.audit.empty": "鏆傛棤瀹¤璁板綍",

  // Admin - llm
  "admin.llm.title": "LLM 接口",
  "admin.llm.addTitle": "添加接口（OpenAI 兼容）",
  "admin.llm.name": "名称",
  "admin.llm.baseUrl": "Base URL",
  "admin.llm.apiKey": "API Key",
  "admin.llm.model": "模型",
  "admin.llm.maxTokens": "最大 Token",
  "admin.llm.temperature": "温度",
  "admin.llm.isDefault": "默认",
  "admin.llm.enabled": "已启用",
  "admin.llm.list": "现有接口",
  "admin.llm.empty": "暂无 LLM 接口",

  // Admin - members
  "admin.members.title": "成员",
  "admin.members.addTitle": "添加用户",
  "admin.members.username": "用户名",
  "admin.members.display": "昵称",
  "admin.members.email": "邮箱",
  "admin.members.password": "密码",
  "admin.members.org": "组织",
  "admin.members.active": "已激活",
  "admin.members.empty": "暂无用户",

  // Admin - channels
  "admin.channels.title": "通道",
  "admin.channels.addTitle": "添加通道",
  "admin.channels.kind": "类型",
  "admin.channels.name": "名称",
  "admin.channels.credentials": "凭据 (JSON)",
  "admin.channels.list": "现有通道",
  "admin.channels.reload": "重载",
  "admin.channels.status": "状态",
  "admin.channels.enabled": "已启用",
  "admin.channels.lastSeen": "最后活跃",
  "admin.channels.listener": "监听器",
  "admin.channels.empty": "暂无通道",
  "admin.channels.running": "运行中",
    "admin.channels.runningCount": "运行中：{count}",
    "admin.channels.hint": "提示：使用 <code>echo</code> 类型可通过 <code>POST /api/webhook/echo</code> 进行进程内测试。",
  "admin.channels.stopped": "未运行",

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
  "admin.sessions.title": "会话",
  "admin.sessions.allChannels": "全部通道",
  "admin.sessions.title2": "标题",
  "admin.sessions.user": "用户",
  "admin.sessions.channel": "通道",
  "admin.sessions.messages": "消息数",
  "admin.sessions.status": "状态",
  "admin.sessions.lastActivity": "最后活跃",
  "admin.sessions.empty": "暂无会话",
  "admin.sessions.archived": "已归档",
  "admin.sessions.web": "网页",
  "admin.sessions.archive": "归档",
  "admin.sessions.delete": "删除",

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












