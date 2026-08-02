# Regulação Polivagal — plataforma psicoeducativa

Aplicação estática, mobile-first e local-first para momentos de alta ativação, desligamento ou instabilidade emocional. Foi projetada para GitHub Pages e não depende de backend, framework, CDN ou serviço externo.

## Escopo clínico

A aplicação usa a Teoria Polivagal como **modelo psicoeducativo**, não como diagnóstico fisiológico. Evita afirmar que uma prática “ativa diretamente o vago ventral” ou mede “estado vagal”. O conteúdo enfatiza estratégias de baixo risco e baixa carga cognitiva: orientação sensorial, respiração lenta sem retenção, pressão/apoiamento, movimento suave, contraste térmico não extremo e conexão social.

## Funcionalidades

- fluxo “Agora” com escolha de estado e intensidade;
- recomendação contextual de prática;
- 8 práticas guiadas com timer;
- voz opcional via Web Speech API;
- rechecagem de intensidade antes/depois;
- histórico local com resumo de resposta percebida;
- mapa pessoal de regulação salvo apenas no navegador;
- plano de apoio com contato local opcional;
- exportação dos registros em JSON;
- tema claro/escuro;
- ampliação de fonte;
- acessibilidade por teclado, ARIA e `prefers-reduced-motion`;
- PWA instalável e funcionamento offline;
- Content Security Policy restritiva;
- nenhum dado enviado a servidor.

## Privacidade

Os dados do mapa pessoal e histórico são persistidos em `localStorage`. Isso significa que ficam no navegador/dispositivo e podem ser acessíveis a outras pessoas que usem o mesmo perfil do navegador. A interface alerta o paciente a não salvar dados pessoais em dispositivos compartilhados.

Não use GitHub Pages para prontuário, anotações clínicas identificáveis, diagnósticos ou outras informações protegidas.

## Estrutura

- `index.html` — estrutura semântica e diálogos;
- `styles.css` — design system responsivo;
- `app.js` — navegação, práticas, timer, armazenamento local, PWA e acessibilidade;
- `sw.js` — cache offline;
- `manifest.webmanifest` — instalação como PWA;
- `assets/icon.svg` — ícone local.

## Publicação no GitHub Pages

1. Envie os arquivos para a branch `main`.
2. Em **Settings → Pages**, selecione **Deploy from a branch**.
3. Use a branch `main` e a pasta `/ (root)`.
4. Aguarde a publicação no endereço `https://ricmurtapsicologia.github.io/regulacao-polivagal./`.

## Validação recomendada antes de uso clínico

- revisar o texto clínico final;
- configurar identidade visual e contato profissional apenas se desejado;
- testar em Android/iOS e desktop;
- executar Lighthouse (Accessibility, Best Practices, SEO e PWA);
- testar navegação apenas por teclado e leitor de tela;
- revisar avisos de segurança conforme população atendida e regras locais.

## Base científica resumida

- Laborde S. et al. *Effects of voluntary slow breathing on heart rate and heart rate variability: A systematic review and a meta-analysis.* Neuroscience & Biobehavioral Reviews. 2022.
- Zaccaro A. et al. *How Breath-Control Can Change Your Life: A Systematic Review on Psycho-Physiological Correlates of Slow Breathing.* Frontiers in Human Neuroscience. 2018.
- Russo M.A. et al. *The physiological effects of slow breathing in the healthy human.* Breathe. 2017.
- Revisões recentes sobre Teoria Polivagal discutem aplicações clínicas e também limitações/controvérsias quanto a especificidade anatômica, RSA e interpretação de marcadores autonômicos.

## Nota

Ferramenta psicoeducativa complementar. Não realiza diagnóstico, monitoramento fisiológico ou atendimento de emergência.
