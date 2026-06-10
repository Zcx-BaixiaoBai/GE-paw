// GE-paw Console i18n. Currently zh-CN only; the table is centralized
// so future locales can be added without touching every component.
export type Locale = "zh-CN";

export const dict = {
  // Brand
  "brand.name": "GE-paw",
  "brand.tagline": "代理空间 · 本地运行",
  "favicon.title": "GE-paw 控制台",

  // Top bar
  "topbar.workspace": "工作区",
  "topbar.newThread": "新建会话",
  "topbar.untitledThread": "未命名会话",
  "topbar.toggleLeft": "切换左侧面板 (Ctrl+B)",
  "topbar.toggleRight": "切换右侧面板 (Ctrl+J)",
  "topbar.toggleTheme": "切换主题",
  "topbar.logout": "退出登录",
  "topbar.role.admin": "管理员",
  "topbar.role.member": "成员",
  "topbar.theme.dark": "深色主题",
  "topbar.theme.light": "浅色主题",
  "topbar.theme.system": "跟随系统",
  "topbar.menu.profile": "个人资料",
  "topbar.menu.settings": "设置",
  "topbar.menu.admin": "管理后台",
  "topbar.menu.signout": "退出",
  "topbar.rename": "重命名会话",
  "topbar.rename.placeholder": "会话标题",
  "topbar.archive": "归档会话",
  "topbar.unarchive": "取消归档",
  "topbar.pin": "固定到顶部",
  "topbar.unpin": "取消固定",

  // Left pane
  "left.newSession": "新建会话",
  "left.section.modes": "模式",
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
  "tab.empty.hint": "在主聊天页输入 + 新建标签",
  "tab.menu.open": "打开标签页",
  "tab.menu.kbd.live": "可用",
  "tab.menu.kbd.soon": "即将",
  "tab.none": "无标签页",
  "tab.files.hint": "工作区与知识库树",
  "tab.web.hint": "在外部网页中浏览 URL，便于审阅对话引用",
  "tab.diff.hint": "对比本会话中编辑过的文件改动",
  "tab.preview.hint": "多格式知识库预览",
  "tab.plan.hint": "助手生成的可验证计划步骤",
  "tab.goals.hint": "当前会话的可验证目标",

  // Plan tab / drawer
  "plan.session": "会话",
  "plan.sessionPlaceholder": "会话 ID",
  "plan.load": "加载",
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
  "goals.status.label": "状态",
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
  "chat.thinking.toggle": "展开/收起",
  "chat.tool.label": "工具调用",
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
  "perm.changed": "权限已更新",

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
  "admin.crons.title": "定时任务",
  "admin.crons.addTitle": "添加任务",
  "admin.crons.name": "名称",
  "admin.crons.schedule": "调度表达式 (cron)",
  "admin.crons.prompt": "提示词模板",
  "admin.crons.lastStatus": "上次状态",
  "admin.crons.lastRun": "上次运行",
  "admin.crons.nextRun": "下次运行",
  "admin.crons.failures": "连续失败",
    "admin.crons.enable": "启用",
    "admin.crons.disable": "禁用",
    "admin.crons.hint": "输出会记录到 cron_run 并计入 token_usage_log。连续 3 次失败会自动禁用任务。",
  "admin.crons.empty": "暂无定时任务",

  // Admin - tokens
  "admin.tokens.title": "Token 用量",
  "admin.tokens.window": "窗口",
  "admin.tokens.last24h": "最近 24 小时",
  "admin.tokens.last7d": "最近 7 天",
  "admin.tokens.last30d": "最近 30 天",
  "admin.tokens.last90d": "最近 90 天",
  "admin.tokens.byModel": "按模型",
  "admin.tokens.byDay": "按日",
  "admin.tokens.byUser": "按用户",
  "admin.tokens.calls": "调用次数",
  "admin.tokens.prompt": "输入 Token",
  "admin.tokens.completion": "输出 Token",
  "admin.tokens.total": "总 Token",
  "admin.tokens.cost": "费用 (分)",
    "admin.tokens.summary": "总计 {calls} 次调用 / {tokens} tokens / {cents} 分",
    "admin.tokens.emptyWindow": "当前窗口暂无数据。",
    "admin.tokens.knownHint": "已知默认价格：{models}",
  "admin.tokens.empty": "暂无用量",
  "admin.tokens.monthToDate": "本月累计",
  "admin.tokens.costTable": "费用表",

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
  "admin.wiki.title": "知识库（服务端语料）",
  "admin.wiki.upload": "上传",
  "admin.wiki.triggerIngest": "触发导入",
  "admin.wiki.compileIndex": "构建索引",
  "admin.wiki.resetAll": "清空全部",
  "admin.wiki.path": "路径",
  "admin.wiki.status": "状态",
  "admin.wiki.size": "大小",
  "admin.wiki.error": "错误",
  "admin.wiki.empty": "暂无上传",
  "admin.wiki.log": "日志",
  "admin.wiki.uploadHint": "支持 txt / md / pdf / docx 上传后由服务端解析和嵌入",
  "admin.wiki.confirmReset": "确定清空全部知识库源与页面吗？",
  "admin.wiki.logUploaded": "已上传：{path}",
  "admin.wiki.logUploadFailed": "上传失败：{err}",
  "admin.wiki.logIngest": "导入：{result}",
  "admin.wiki.logIngestFailed": "导入失败：{err}",
  "admin.wiki.logCompile": "构建索引：{result}",
  "admin.wiki.logCompileFailed": "构建索引失败：{err}",
  "admin.wiki.logReset": "已清空",
  "admin.wiki.logResetFailed": "清空失败：{err}",

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












