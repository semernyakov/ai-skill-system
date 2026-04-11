import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { api } from '../src/services/api';

describe('API Service', () => {
  beforeEach(() => {
    // Reset API base URL before each test
    api.setBaseUrl('http://127.0.0.1:8000/api/v1');
  });

  describe('Rules API', () => {
    it('should list rules', async () => {
      const rules = await api.listRules();
      expect(Array.isArray(rules)).toBe(true);
    });

    it('should create a rule', async () => {
      const newRule = await api.createRule({
        name: 'test-rule',
        description: 'Test rule',
        globs: ['**/*.py'],
        always_apply: false
      });
      expect(newRule).toHaveProperty('id');
      expect(newRule.name).toBe('test-rule');
    });

    it('should get a rule by ID', async () => {
      // First create a rule
      const created = await api.createRule({
        name: 'test-rule-get',
        description: 'Test rule',
        globs: ['**/*.py'],
        always_apply: false
      });
      
      const rule = await api.getRule(created.id);
      expect(rule.id).toBe(created.id);
    });

    it('should update a rule', async () => {
      const created = await api.createRule({
        name: 'test-rule-update',
        description: 'Test rule',
        globs: ['**/*.py'],
        always_apply: false
      });
      
      const updated = await api.updateRule(created.id, {
        name: 'updated-rule',
        description: 'Updated description'
      });
      expect(updated.name).toBe('updated-rule');
    });

    it('should delete a rule', async () => {
      const created = await api.createRule({
        name: 'test-rule-delete',
        description: 'Test rule',
        globs: ['**/*.py'],
        always_apply: false
      });
      
      await api.deleteRule(created.id);
      // Should not throw
    });
  });

  describe('Skills API', () => {
    it('should list skills', async () => {
      const skills = await api.listSkills();
      expect(Array.isArray(skills)).toBe(true);
    });

    it('should create a skill', async () => {
      const newSkill = await api.createSkill({
        name: 'test-skill',
        description: 'Test skill'
      });
      expect(newSkill).toHaveProperty('id');
      expect(newSkill.name).toBe('test-skill');
    });

    it('should get a skill by ID', async () => {
      const created = await api.createSkill({
        name: 'test-skill-get',
        description: 'Test skill'
      });
      
      const skill = await api.getSkill(created.id);
      expect(skill.id).toBe(created.id);
    });

    it('should update a skill', async () => {
      const created = await api.createSkill({
        name: 'test-skill-update',
        description: 'Test skill'
      });
      
      const updated = await api.updateSkill(created.id, {
        name: 'updated-skill',
        description: 'Updated description'
      });
      expect(updated.name).toBe('updated-skill');
    });

    it('should delete a skill', async () => {
      const created = await api.createSkill({
        name: 'test-skill-delete',
        description: 'Test skill'
      });
      
      await api.deleteSkill(created.id);
      // Should not throw
    });
  });

  describe('MCP API', () => {
    it('should list MCP services', async () => {
      const services = await api.listMCP();
      expect(Array.isArray(services)).toBe(true);
    });

    it('should start an MCP service', async () => {
      const result = await api.startMCP('test-service');
      expect(result).toHaveProperty('message');
    });

    it('should stop an MCP service', async () => {
      const result = await api.stopMCP('test-service');
      expect(result).toHaveProperty('message');
    });

    it('should check MCP health', async () => {
      const health = await api.checkMCPHealth();
      expect(typeof health).toBe('object');
    });
  });

  describe('Audit API', () => {
    it('should run an audit', async () => {
      const result = await api.runAudit({
        audit_type: 'security'
      });
      expect(result).toHaveProperty('id');
    });

    it('should list audit results', async () => {
      const results = await api.listAuditResults();
      expect(Array.isArray(results)).toBe(true);
    });

    it('should get audit result by ID', async () => {
      const created = await api.runAudit({ audit_type: 'security' });
      const result = await api.getAuditResult(created.id);
      expect(result.id).toBe(created.id);
    });
  });

  describe('Sync API', () => {
    it('should run sync', async () => {
      const result = await api.runSync({ source: 'test' });
      expect(result).toHaveProperty('status');
    });

    it('should get sync status', async () => {
      const status = await api.getSyncStatus();
      expect(status).toHaveProperty('status');
    });
  });

  describe('Logs API', () => {
    it('should view logs', async () => {
      const logs = await api.viewLogs({ limit: 10 });
      expect(Array.isArray(logs)).toBe(true);
    });
  });
});
