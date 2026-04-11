import { describe, it, expect, vi } from 'vitest';

// Mock fetch globally
global.fetch = vi.fn();

describe('API Service', () => {
  it('should have listRules function', () => {
    const { api } = require('../src/services/api');
    expect(typeof api.listRules).toBe('function');
  });

  it('should have createRule function', () => {
    const { api } = require('../src/services/api');
    expect(typeof api.createRule).toBe('function');
  });

  it('should have listSkills function', () => {
    const { api } = require('../src/services/api');
    expect(typeof api.listSkills).toBe('function');
  });

  it('should have createSkill function', () => {
    const { api } = require('../src/services/api');
    expect(typeof api.createSkill).toBe('function');
  });

  it('should have listMCP function', () => {
    const { api } = require('../src/services/api');
    expect(typeof api.listMCP).toBe('function');
  });
});
