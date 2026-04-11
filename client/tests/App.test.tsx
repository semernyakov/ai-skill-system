import { describe, it, expect } from 'vitest';

describe('App', () => {
  it('should be importable', () => {
    const App = require('../src/App').default;
    expect(App).toBeDefined();
  });
});
