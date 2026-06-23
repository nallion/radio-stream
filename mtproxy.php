<?php

$file = __FILE__;

// читаем всё после __halt_compiler()
$fp = fopen($file, "r");
fseek($fp, __COMPILER_HALT_OFFSET__);

$data = stream_get_contents($fp);
fclose($fp);

$lines = array_filter(array_map('trim', explode("\n", $data)));

shuffle($lines);

echo implode(PHP_EOL, $lines);

__halt_compiler();
tg-gw.com:443:ddd1a377f2cc4884c05fcd433dbf7089bd
85.155.101.63:443:77e616b89815f53b5a2d2d4299fc7ede
ams1.tlgfast.com:443:083fe0c452e2407d835537872f097c54
tg.towersflowerss.com:443:90eba2e23b01f1cb32b4b9e29bbd7f80
109.236.50.155:443:ee7777772e676f6f676c652e636f6db0
edge-eu1.climaxvpn.com:443:ddbb01e59aa510ca70ce9e935c471df2d8
tg.tokervpn.ru:443:ab02774b212bf41c19f8f00ab895e2db
tg.atomic-vpn.com:443:dd3f087f3f403449a2a9446de22b5bc3d1
138.124.70.86:443:6356ebb33a57b6deda8a1c3cf2aee557
balance-ee.elix.rip:443:77e616b89815f53b5a2d2d4299fc7ede
guard-3.secureservice.top:443:422c2d5e28f48282a4e2dfaea14fd5a9
guard-2.secureservice.top:443:c63135841f7e17e5d44e63b0de7ce8e6
mtproxy.kitty-vpn.net:443:99716ffe32242603e8858eef955f2262
138.124.71.179:443:6356ebb33a57b6deda8a1c3cf2aee557
proxy.star-v.ru:443:ddb632d68d9b00d674cb64265a2e23e98d
204.168.145.16:443:8f604a7e17871ca0b6e39e5435ac2e10
proxy.vpncitadel.id:443:04a421876006fc121651796f14540455
tg.unibot.work:443:dd4d90d8c4c45d25aa849135d4e73c27c7
138.124.72.27:443:6356ebb33a57b6deda8a1c3cf2aee557
mtproto.elix.rip:443:77e616b89815f53b5a2d2d4299fc7ede
ffastdomain-eu.com:443:afdc38b8068b2444e50f6a4f093751b5
166.1.160.127:443:6356ebb33a57b6deda8a1c3cf2aee557  
