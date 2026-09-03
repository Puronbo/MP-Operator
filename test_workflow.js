export const meta = {
  name: 'test-workflow',
  description: 'Test workflow',
  phases: [{ title: 'Test', detail: 'Test phase' }]
};

phase('Test');
return 'test result';