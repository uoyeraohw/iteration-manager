const task = await taskSpace("iteration10-self-hosting-board-20261114");
const page = task.page("p1");
console.log(JSON.stringify({spaceId:task.spaceId,page:page.label,info:await page.info()}));
console.log(await page.snapshot());

