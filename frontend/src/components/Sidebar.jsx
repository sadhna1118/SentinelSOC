import React from 'react';
import { 
  LayoutDashboard, 
  Terminal, 
  AlertTriangle, 
  Briefcase, 
  Sliders, 
  Search, 
  Cpu, 
  Network,
  FileCode2 
} from 'lucide-react';

export function Sidebar({ activeTab, onTabChange, metrics }) {
  const navItems = [
    { id: 'dashboard', label: 'Operations Center', icon: LayoutDashboard },
    { id: 'logs', label: 'SIEM Log Explorer', icon: Terminal, count: metrics?.total_logs_ingested },
    { id: 'alerts', label: 'Security Alerts', icon: AlertTriangle, count: metrics?.active_open_alerts, badgeClass: 'critical' },
    { id: 'incidents', label: 'Incident Workbench', icon: Briefcase, count: metrics?.open_incidents },
    { id: 'rules', label: 'Detection Rules', icon: Sliders },
    { id: 'threat-intel', label: 'Threat Intel Hub', icon: Search },
    { id: 'cyberchef', label: 'CyberChef Toolkit', icon: FileCode2 },
    { id: 'mitre', label: 'MITRE ATT&CK Matrix', icon: Network },
    { id: 'pcap', label: 'Wireshark / PCAP', icon: Cpu },
  ];

  return (
    <aside className="sidebar">
      <div style={{ padding: '16px 14px 4px', fontSize: '11px', fontWeight: '700', color: 'var(--text-muted)', letterSpacing: '0.1em' }}>
        MONITORING & INVESTIGATION
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <div
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onTabChange(item.id)}
            >
              <Icon size={18} color={item.highlight && !isActive ? 'var(--color-high)' : undefined} />
              <span className="nav-label">{item.label}</span>
              {item.count !== undefined && item.count > 0 && (
                <span className={`nav-badge ${item.badgeClass || 'count'}`}>
                  {item.count}
                </span>
              )}
            </div>
          );
        })}
      </nav>

      <div style={{ padding: '14px', borderTop: '1px solid var(--border-subtle)', fontSize: '11px', color: 'var(--text-muted)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
          <span>SOC Analyst</span>
          <span className="mono" style={{ color: 'var(--color-cyan)' }}>L2 Active</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>Engine</span>
          <span className="mono" style={{ color: 'var(--color-success)' }}>ONLINE</span>
        </div>
      </div>
    </aside>
  );
}
