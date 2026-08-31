# N3 Natural — Regulação Polivagal

Versão: `n3-20260831` • Perfil: `N3-C experiential`.

Nesta plataforma a pausa é parte da intervenção. O motor distingue pausa linguística de pausa experiencial. Instruções corporais, de atenção, respiração e observação recebem tempo suficiente para execução, com variação semântica e determinística em vez de intervalos repetitivos.

Regras: Neural TTS pt-BR; `pt-BR-AntonioNeural`; mono 44,1 kHz; MP3 128 kbps; -18 dBFS; pico <= -1,2 dBFS; compressão leve; sem ambiente, trilha ou Foley; sem `speechSynthesis` do navegador. A pasta `audio/n2/` permanece como rollback. A master canônica é `audio/n3/`.

Compatibilidade: enquanto `app-core.js` conservar chamadas ao identificador histórico `RC_AUDIO_N2`, o carregador N3 pode expor esse nome como alias para `RC_AUDIO_N3`. Isso não significa uso de áudio N2; é apenas compatibilidade de API interna e deve ser documentado no manifesto.
