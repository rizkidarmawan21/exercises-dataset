import { test, expect } from '@playwright/test';

test('mobile: filter area stays fixed and result list scrolls', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`file:///home/hermes/exercises-dataset/index.html`);
  await expect(page.locator('#results-count')).toContainText('exercises');
  const main = page.locator('.main-content');
  await main.evaluate((el) => {
    const r = el.getBoundingClientRect();
    if (r.height <= 0 || r.width <= 0) throw new Error('main-content has zero size');
  });
  await expect(page.locator('#exercise-grid .exercise-card').first()).toBeInViewport();
});
