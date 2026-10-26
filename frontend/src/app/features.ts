export const NUMERIC_FIELDS: string[] = [
  'dur', 'rate', 'sbytes', 'dbytes', 'sttl', 'sload', 'dload', 'dloss',
  'smeansz', 'dmeansz', 'Sintpkt', 'Dintpkt', 'Sjit', 'djit',
  'tcprtt', 'synack', 'ackdat', 'ct_state_ttl', 'ct_srv_src', 'ct_srv_dst',
  'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_src_dport_ltm',
];

export const CATEGORICAL_FIELDS: { name: string; options: string[] }[] = [
  { name: 'proto', options: ['tcp', 'udp', 'icmp', 'arp', 'ospf', 'igmp', 'sctp'] },
  { name: 'service', options: ['-', 'http', 'ftp', 'ftp-data', 'smtp', 'ssh', 'dns', 'pop3', 'ssl', 'snmp', 'dhcp', 'irc', 'radius'] },
  { name: 'state', options: ['FIN', 'CON', 'INT', 'REQ', 'RST', 'ECO', 'ACC', 'CLO'] },
];

export const SAMPLE: Record<string, number | string> = {
  dur: 0.000011, rate: 90909.0902, sbytes: 496, dbytes: 0, sttl: 254, sload: 180363632,
  dload: 0, dloss: 0, smeansz: 248, dmeansz: 0, Sintpkt: 0.011, Dintpkt: 0, Sjit: 0,
  djit: 0, tcprtt: 0, synack: 0, ackdat: 0, ct_state_ttl: 2, ct_srv_src: 2, ct_srv_dst: 2,
  ct_dst_sport_ltm: 1, ct_dst_src_ltm: 2, ct_src_dport_ltm: 1,
  proto: 'udp', service: '-', state: 'INT',
};
