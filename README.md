# Regulação em Crises — v2.0.0

Aplicação psicoeducativa, mobile-first e local-first para apoiar pacientes em momentos de desregulação emocional. A plataforma integra três lentes clínicas complementares:

- **Teoria Polivagal como mapa psicoeducativo** para organizar experiências de segurança, mobilização e desligamento, sem diagnosticar estados vagais ou afirmar ativação direta de vias autonômicas específicas;
- **DBT/TCD como tecnologia de manejo da crise**, priorizando mindfulness breve, tolerância ao mal-estar, redução de impulsividade, adiamento de decisões e recuperação de controle comportamental;
- **ACT como tecnologia de flexibilidade psicológica**, usando aceitação, desfusão, contato com o presente, valores e ação comprometida quando já existe alguma margem de escolha.

## Arquitetura clínica

A sequência principal é:

**Perceber → Não piorar → Regular → Escolher**

A interface distingue duas medidas:

1. **Intensidade emocional (0–10)** — quão forte está a experiência;
2. **Margem de escolha (0–10)** — quanto espaço existe entre sentir a urgência e agir.

A redução de sintomas não é tratada como único indicador de sucesso. Uma prática também pode ser útil quando a emoção continua presente, mas o paciente recupera maior capacidade de escolher uma resposta segura e coerente.

## Modo Agora

O fluxo agudo foi desenhado com baixa carga cognitiva. O paciente:

1. identifica se está mais acelerado, desligado ou com alguma estabilidade;
2. informa intensidade e margem de escolha;
3. recebe uma habilidade contextual;
4. realiza uma orientação guiada curta;
5. reavalia intensidade e margem de escolha;
6. pode registrar o resultado localmente.

A plataforma reforça uma distinção central:

> Crise e problema não são a mesma coisa. O problema pode ser real e importante sem precisar ser resolvido no pico da emoção.

## Habilidades disponíveis

### DBT/TCD
- STOP — não agir no automático;
- adiar decisão importante;
- observar a urgência como uma onda;
- mente sábia: emoção + fatos + valores.

### Recursos corporais e de orientação
- expiração suavemente mais longa, sem retenção;
- orientação pelos sentidos;
- pressão e apoio corporal;
- movimento pequeno e orientado;
- temperatura confortável, sem extremos.

### ACT
- nomear sem discutir com a mente — desfusão;
- próxima ação guiada por valores.

### Conexão
- organização de contato com pessoa segura e previsível.

Todas as práticas podem ser interrompidas. Técnicas respiratórias não devem ser forçadas; se houver tontura, falta de ar ou piora do desconforto, a orientação é retornar à respiração espontânea.

## Meu mapa

O paciente pode registrar localmente:

- sinais iniciais de aceleração;
- sinais iniciais de desligamento;
- frase de orientação;
- pessoa de confiança e contato;
- lugar previsível para reorganização;
- recursos que costumam ajudar;
- fatores que convém reduzir durante uma crise;
- valores e aspectos da vida que deseja proteger mesmo quando está emocionalmente desorganizado.

## Depois da onda

A seção **Depois** utiliza uma análise funcional simplificada, inspirada em DBT/TCD, sem transformar a aplicação em prontuário. O paciente pode observar:

- contexto;
- primeiros sinais corporais;
- urgência comportamental;
- habilidade utilizada;
- recurso que ajudou;
- sinal que poderá reconhecer mais cedo em uma próxima situação.

## Histórico

Os registros mostram tanto a mudança de intensidade quanto a mudança na margem de escolha. Não há gamificação, streak, medalha ou pontuação de desempenho.

## Vídeo complementar

A seção **Entender** inclui uma prática de mindfulness do Programa **Pausa para um Respiro**, da Faculdade de Letras da UFMG, hospedada no YouTube.

O vídeo aparece apenas na área educativa e é apresentado como prática programada para momentos de estabilidade. Não é colocado como primeira intervenção durante o pico de uma crise.

A incorporação utiliza `youtube-nocookie.com` para reduzir rastreamento antes da interação com o player.

## Identidade profissional

A interface identifica o recurso como pertencente a **Richelmy Murta · Psicologia Clínica**.

O rodapé inclui:

- Richelmy Murta;
- Psicólogo clínico;
- Psicoterapia baseada em evidências · TCC · ACT · DBT/TCD · Regulação emocional;
- convite clínico discreto para levar as observações à terapia;
- aviso de que o recurso é complementar e não substitui acompanhamento psicológico ou atendimento de emergência.

## Privacidade

A aplicação não possui backend.

Mapa pessoal, registros de práticas e reflexões pós-crise ficam somente no `localStorage` do navegador. Isso significa que podem ser acessíveis a outras pessoas que utilizem o mesmo perfil do dispositivo.

Não utilize esta página para prontuário, diagnóstico, documentos clínicos identificáveis ou qualquer outra informação que deva ser armazenada em sistema clínico protegido.

## Segurança clínica

A plataforma não:

- diagnostica estado autonômico;
- mede tônus vagal;
- promete ativar diretamente o nervo vago;
- substitui avaliação profissional;
- substitui atendimento presencial de urgência ou emergência;
- deve ser utilizada como único recurso quando a pessoa não consegue permanecer segura.

Nessas situações, a interface orienta aumentar presença humana e procurar atendimento presencial apropriado.

## Acessibilidade e UX

- mobile-first;
- botões com área de toque ampla;
- navegação por teclado;
- ARIA em controles principais;
- contraste claro/escuro;
- ampliação de fonte;
- suporte a `prefers-reduced-motion`;
- voz opcional nas práticas guiadas;
- conteúdo científico separado do fluxo agudo;
- instruções de uma ação por vez durante as práticas.

## PWA e funcionamento offline

A aplicação possui:

- `manifest.webmanifest`;
- service worker;
- cache local dos recursos essenciais;
- instalação como aplicativo quando suportada pelo navegador.

Versão do cache: **v2.0.0**.

O player do YouTube requer conexão com a internet e não faz parte do cache offline.

## Estrutura

- `index.html` — interface e conteúdo clínico;
- `styles.css` — design system responsivo;
- `app.js` — roteamento, recomendações, práticas, timers e armazenamento local;
- `sw.js` — cache offline;
- `manifest.webmanifest` — metadados da PWA;
- `assets/icon.svg` — ícone local;
- `.nojekyll` — publicação estática sem processamento Jekyll;
- `.github/workflows/pages.yml` — workflow de publicação quando GitHub Pages por Actions estiver habilitado.

## Base científica resumida

- Linehan, M. M. *DBT Skills Training Manual*. 2ª ed. Guilford Press, 2015.
- Hayes, S. C.; Strosahl, K. D.; Wilson, K. G. *Acceptance and Commitment Therapy: The Process and Practice of Mindful Change*. 2ª ed. Guilford Press, 2012.
- Macri, J. A.; Rogge, R. D. Psychological flexibility and inflexibility as treatment mechanisms in Acceptance and Commitment Therapy. *Clinical Psychology Review*, 2024.
- Laborde, S. et al. Effects of voluntary slow breathing on heart rate and heart rate variability: a systematic review and meta-analysis. *Neuroscience & Biobehavioral Reviews*, 2022.
- Zaccaro, A. et al. How Breath-Control Can Change Your Life: a systematic review on psycho-physiological correlates of slow breathing. *Frontiers in Human Neuroscience*, 2018.

A Teoria Polivagal é utilizada como linguagem clínica e psicoeducativa. Alguns aspectos neuroanatômicos, evolutivos e métricos associados ao modelo permanecem em discussão científica; por isso a plataforma evita inferências fisiológicas específicas a partir da experiência subjetiva do paciente.

## Publicação

Origem prevista: branch `main`, raiz `/`, via GitHub Pages.

> Observação: o repositório atualmente foi criado com o nome `regulacao-polivagal.` (com ponto final). Para uma URL pública mais limpa, recomenda-se renomeá-lo administrativamente para `regulacao-polivagal`.
