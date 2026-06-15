const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('正在打开页面...');
  await page.goto('http://localhost:5173/app/admin/llm');
  
  console.log('等待页面加载...');
  await page.waitForLoadState('networkidle');
  
  console.log('获取页面标题...');
  const title = await page.title();
  console.log('页面标题:', title);
  
  console.log('获取页面内容...');
  const content = await page.content();
  
  console.log('页面内容前500字符:', content.substring(0, 500));
  
  console.log('检查页面关键元素...');
  const elements = await page.evaluate(() => {
    const results = {};
    
    // 检查是否有供应商卡片网格
    const providerCards = document.querySelectorAll('[class*="provider"], [class*="card"], [class*="grid"]');
    results.providerCards = providerCards.length;
    
    // 检查是否有配置面板
    const configPanels = document.querySelectorAll('[class*="config"], [class*="panel"], [class*="form"]');
    results.configPanels = configPanels.length;
    
    // 检查是否有输入框
    const inputs = document.querySelectorAll('input, select, textarea');
    results.inputs = inputs.length;
    
    // 检查是否有按钮
    const buttons = document.querySelectorAll('button');
    results.buttons = buttons.length;
    
    // 检查页面主要内容
    const mainContent = document.querySelector('main, [class*="main"], [class*="content"]');
    results.hasMainContent = !!mainContent;
    
    // 检查是否有登录表单
    const loginForm = document.querySelector('form[action*="login"], [class*="login"], [class*="sign-in"]');
    results.hasLoginForm = !!loginForm;
    
    // 检查页面文本内容
    const bodyText = document.body.innerText;
    results.bodyTextLength = bodyText.length;
    
    return results;
  });
  
  console.log('页面元素统计:', elements);
  
  await browser.close();
  console.log('页面检查完成');
})();
