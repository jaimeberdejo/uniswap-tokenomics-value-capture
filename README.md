# UNI tras la UNIfication: ¿captura de valor real o teatro tokenómico?

**Un análisis on-chain del mecanismo *buy-and-burn* de Uniswap.**

Proyecto final del **módulo de Blockchain** del Máster en **Inteligencia Artificial aplicada a los Mercados Financieros**. Estudia si la captura de valor de **UNI** —activada en diciembre de 2025 con el *fee switch* y el mecanismo de quema (**UNIfication**)— es **real, material y sostenible**, usando datos on-chain generados por el autor y una capa de análisis de IA.

> **Pregunta de investigación:** ¿el *buy-and-burn* de UNI genera captura de valor real para los holders?
>
> **Veredicto (resumen):** la captura de valor es **real, modesta y de sostenibilidad aún no demostrada**. La quema es genuina y deja la oferta neta deflacionaria (emisión cero, ~106,2M UNI quemados), pero es pequeña (~$49,6M/año, ~1,83% de *burn yield*), llega a los holders solo de forma indirecta (vía escasez, no como dividendo), y su sostenibilidad depende del volumen futuro y de una política de gobernanza revocable.

📄 **Informe completo:** [`analysis/05-report.pdf`](analysis/05-report.pdf) (en español, ~24 páginas)
📊 **Dashboard público (Dune):** https://dune.com/jbs19022909/uni-value-capture-after-unification
📓 **Notebook reproducible:** [`notebooks/04-ml-analysis.ipynb`](notebooks/04-ml-analysis.ipynb) — corre de principio a fin desde los CSV cacheados, **sin clave de Dune**.

---

## Métricas clave (data-as-of 2026-06-21)

| Métrica | Resultado | Interpretación |
|---|---|---|
| UNI quemado (acumulado) | ~106,2M UNI | Reducción real de la oferta |
| Quema anual en curso | ~$49,6M/año | Real, pero no enorme |
| Burn yield | ~1,83% | Modesto frente al market cap |
| Market cap | ~$2,71B | Listón alto para ser material |
| Movimiento del precio de UNI | $5,96 → ~$3 | El mercado aún no está convencido |
| Volumen actual | ~$0,70B/día | Por debajo del break-even |
| Volumen de break-even | ~$2,11B/día | Sostenibilidad no demostrada |

La quema única de 100M UNI (~$595,6M) se ejecutó el **27 de diciembre de 2025 (UTC)** — la inflexión que estructura todo el análisis.

---

## Metodología — análisis por fases

El proyecto sigue una disciplina deliberada: **primero los datos, después la IA**. Las dos primeras fases construyen el fundamento y la evidencia; las dos últimas son capas de IA **aditivas e interpretables** que afinan la lectura sin sustituir la evidencia on-chain (el veredicto se sostiene aunque se eliminen las fases 3 y 4).

1. **Fundamento tokenómico** — el problema de captura de valor de UNI; diferencia entre comisiones LP, comisiones de protocolo y valor que llega al holder; qué cambió con UNIfication.
2. **Evidencia on-chain** — extracción vía SQL en Dune → CSV → dashboard público. *Evidencia principal del informe.*
3. **AI-Light (interpretación + stress-test)** — la IA estructura la interpretación y somete el veredicto a sus objeciones más fuertes. *Contrasta el veredicto; no lo genera.*
4. **AI-Medium (machine learning)** — técnicas interpretables (KMeans, IsolationForest, modelo de break-even) para añadir resolución. *Afina la lectura; no sustituye la evidencia.*

La capa de ML usa **scikit-learn** (clustering de holders, detección de anomalías) y un modelo de break-even del *buy-and-burn*; ninguna técnica es de caja negra y no se hace predicción de precio (fuera de alcance por diseño).

---

## Estructura del repositorio

```
analysis/
  05-report.pdf / .md / .html   # Informe final (ES) + fuente Markdown + HTML autocontenido
  report.css                    # Estilo de impresión (Markdown → HTML → PDF vía pandoc + navegador)
  03-interpretation.md          # Capa AI-Light: interpretación
  03-adversarial-stress-test.md # Capa AI-Light: stress-test adversarial
  figures/                      # Figuras del informe (PNG) generadas por el notebook
notebooks/
  04-ml-analysis.ipynb          # Notebook reproducible (DEL-03) — corre desde data/ sin clave
  04_ml_analysis.py             # Módulo companion del notebook
  _build_ipynb.py               # Reconstruye el .ipynb desde el .py
tests/
  test_04_ml_analysis.py        # Tests del pipeline ML (calibración, k-selección, whitelist)
data/                           # CSV cacheados (datos reales, reproducibles) + MANIFEST + README
queries/                        # SQL versionado: un .sql por panel del dashboard de Dune
scripts/
  export_dune.py                # Exporta resultados de Dune a data/*.csv
```

---

## Reproducir el análisis

Requisitos: Python 3.12+ con `pandas`, `numpy`, `scikit-learn`, `matplotlib` (y `jupyter` para el notebook).

```bash
pip install pandas numpy scikit-learn matplotlib jupyter

# Ejecutar el pipeline ML completo desde los CSV cacheados (sin clave de Dune):
python notebooks/04_ml_analysis.py

# O abrir el notebook:
jupyter notebook notebooks/04-ml-analysis.ipynb

# Tests:
python -m pytest tests/test_04_ml_analysis.py
```

El notebook **no requiere ninguna clave de API**: lee los CSV de `data/`, ya cacheados y versionados. Para **re-extraer** los datos desde cero necesitarías una clave de Dune (ver abajo).

### Re-extraer los datos (opcional)

Copia `.env.example` a `.env`, añade tu clave de Dune, y ejecuta el exportador:

```bash
cp .env.example .env       # rellena DUNE_API_KEY
python scripts/export_dune.py
```

El SQL de cada métrica está en `queries/`. **Nunca** se commitea `.env` (está en `.gitignore`).

---

## Fuentes de datos

- **On-chain (primaria):** [Dune Analytics](https://dune.com) — comisiones, quema, oferta, concentración de holders y poder de voto delegado; precios UNI/ETH/AAVE vía `prices.usd`. SQL versionado en `queries/`.
- **TVL:** [DefiLlama](https://defillama.com) (API pública, sin clave).
- **Contexto / gobernanza:** UNIfication ([blog.uniswap.org/unification](https://blog.uniswap.org/unification)), Propuesta de Gobernanza #93 (Agora), y cobertura pública del *fee switch* y la quema de 100M UNI (dic. 2025).

Cada figura y cifra del informe está sellada con su `data-as-of` (ver `data/MANIFEST.csv`).

---

## Contexto académico y aviso

Trabajo individual del módulo de Blockchain (Máster en IA aplicada a los Mercados Financieros, 2025–2026). Análisis con fines **educativos y de investigación**; **no es asesoramiento financiero ni de inversión**. Las cifras son un *snapshot* on-chain con fecha; re-verifica el estado del *fee switch* antes de fiarte de ellas en una fecha posterior.

Autor: **Jaime Berdejo Sánchez**.
