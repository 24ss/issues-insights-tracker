import { test, expect } from '@playwright/test';

test('happy-path: login → submit issue → list shows it', async ({ page }) => {
  // 1 ─ login screen
  await page.goto('/');
  await page.fill('input[type=email]', 'admin@example.com');
  await page.fill('input[type=password]', 'test1234');
  await page.click('button:has-text("Sign In")');

  // 2 ─ land on dashboard (sidebar visible)
  await expect(page.locator('text=Dashboard')).toBeVisible();

  // 3 ─ go to submit page
  await page.goto('/submit');
  await page.fill('input[placeholder="Title"], input[name="title"]', 'E2E issue');
  await page.fill('textarea', 'issue created by playwright');
  await page.selectOption('select', 'LOW');
  await page.click('button:has-text("Submit")');

  // 4 ─ redirected to /issues and the new issue appears
  await page.waitForURL('/issues');
  await expect(page.locator('text=E2E issue')).toBeVisible();
});
