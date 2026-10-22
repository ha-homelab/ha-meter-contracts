<a id="limits-and-trust-boundary"></a>

# Limites e fronteira de confiança

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/limits.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/limits.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/limits.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/limits.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/limits.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/limits.md" lang="pl" dir="ltr">Polski</a> ·
<a href="limits.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/limits.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/limits.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Este é um validador offline de declarações, não um controlador de proteção, instrumento de teste para eletricistas, serviço de descoberta da instalação elétrica ou integração Home Assistant que executa ações.

- Uma leitura total não permite recuperar a potência simultânea exata de três cargas desconhecidas. Estimativas estatísticas seriam estimativas, não medições adequadas para proteção.
- O âmbito, a proveniência, a direção do sinal e as declarações de calibração são fornecidos pelo operador. Declarações falsas podem fazer um sistema físico inválido parecer estruturalmente válido.
- `complete` significa completo em relação às folhas declaradas, não à instalação verificada independentemente. Um marcador de reinicialização da origem é evidência em que se confia, não uma atestação do dispositivo.
- São suportados W, kW, Wh, kWh, V e A. Não modelamos potência reativa/aparente, álgebra trifásica, saturação de CT, transformadores de tensão, retorno do contador ao início ou tarifas.
- Os membros de uma soma são medidores diretos, não outras somas. Somas de potência exigem marcas temporais alinhadas. Somas de energia exigem uma origem de contador explícita comum e amostras alinhadas.
- Os valores são números finitos de vírgula flutuante. Isto não é contabilidade decimal para faturação. Os fatores de calibração são registados, não aplicados.
- Só são verificadas uma amostra atual e uma anterior opcional. Isto não é uma base histórica, detetor de anomalias ou deriva, nem uma auditoria integral da integridade dos contadores.
- Os tempos da origem HA têm de existir e representar verdadeiramente a aquisição. Tempos de receção da cache não são aceites silenciosamente como substitutos.
- O carregamento JSON/YAML tem limites; a API de biblioteca `audit` espera um `Contract` produzido pelo parser. Não construa dataclasses arbitrárias malformadas a partir de objetos não fiáveis.
- A entrada por ficheiro aceita apenas ficheiros regulares. Rejeita links simbólicos no último componente, FIFO, dispositivos e diretórios, abre sem bloqueio e verifica o descritor aberto antes de ler. Plataformas sem `O_NOFOLLOW` e `O_NONBLOCK` rejeitam ficheiros; aí, use `ha_meter_contracts.reader.loads_document` com uma cadeia já limitada. Links em diretórios ascendentes não são uma fronteira de sandbox. O limite de bytes aplica-se mesmo se o ficheiro crescer durante a leitura.
- Um resultado positivo não comprova o funcionamento físico de relés, válvulas, motores, caudal de bombas ou segurança elétrica. Não são executadas reparações ou novas tentativas automáticas.

As entradas e saídas podem conter IDs de entidades e tempos fornecidos pelo operador. Guarde contratos e exportações reais em privado. O repositório contém apenas exemplos sintéticos. O programa não envia dados, mas redirecionar o relatório para um serviço externo é uma escolha do operador.
