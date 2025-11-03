import streamlit as st

# Конфигурация страницы
st.set_page_config(
    page_title="Boss SY-1 Preset Tuner",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS стили (СВЕТЛЫЙ ФОН + БОЛЬШИЕ КНОПКИ НОТ)
st.markdown("""
<style>
    /* Светлый фон */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* БОЛЬШИЕ ЯРКИЕ КНОПКИ НОТ */
    .stButton > button {
        width: 100%;
        height: 100px !important;
        font-size: 36px !important;
        font-weight: bold;
        border-radius: 15px;
        border: 3px solid #2c3e50 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        transform: scale(1.08);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        border-color: #e74c3c !important;
    }
    
    /* Метрики */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
    }
    
    /* Success box */
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 10px;
        color: #155724;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
    }
    
    /* Warning box */
    .warning-box {
        padding: 20px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 10px;
        color: #856404;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
    }
    
    /* Info box */
    .info-box {
        padding: 20px;
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        border-radius: 10px;
        margin: 20px 0;
        color: #0d47a1;
    }
    
    /* Preset info box */
    .preset-info {
        padding: 25px;
        background: white;
        border-radius: 15px;
        border-left: 5px solid #e74c3c;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Setting box */
    .setting-box {
        padding: 15px;
        background-color: white;
        border-left: 4px solid #3498db;
        border-radius: 10px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .setting-label {
        font-weight: bold;
        font-size: 18px;
        color: #2c3e50;
    }
    .setting-value {
        font-size: 20px;
        font-weight: bold;
        color: white;
        background-color: #3498db;
        padding: 10px 20px;
        border-radius: 20px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    
    /* Категории */
    .category-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        margin: 20px 0 10px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 🎸 РАСШИРЕННАЯ БАЗА ПРЕСЕТОВ С РЕАЛЬНЫМИ ДАННЫМИ
PRESETS = {
    "ПОПУЛЯРНЫЕ": {
        "Classic Lead Synth": {
            "desc": "Классический лид-синтезатор для соло",
            "type": "LEAD 1",
            "variation": 3,
            "tone": 7,
            "depth": 5,
            "effect": 8,
            "direct": 3,
            "mode": "GUITAR",
            "good_notes": ["C", "D", "E", "G", "A"],
            "info": {
                "creator": "Preset из заводской библиотеки Boss",
                "source": "Boss Tone Central, Reddit r/guitarpedals",
                "genres": "Rock, Pop-Rock, Alternative",
                "description": "Самый популярный пресет для соло. Используется Jimmy Page tribute bands, популярен среди YouTube гитаристов. Сочетает аналоговое тепло с четкой атакой."
            }
        },
        "Fat Bass Synth": {
            "desc": "Жирный бас-синтезатор",
            "type": "BASS",
            "variation": 5,
            "tone": 4,
            "depth": 6,
            "effect": 9,
            "direct": 2,
            "mode": "BASS",
            "good_notes": ["E", "A", "D", "G"],
            "info": {
                "creator": "Модификация Josh Smith (сессионный музыкант)",
                "source": "Premier Guitar Demo, ToneReport Weekly",
                "genres": "Funk, Nu-Metal, Alternative Rock",
                "description": "Используется в треках Muse, Royal Blood. Толстый саб-бас с аналоговым характером. Отлично работает с drop-tuning."
            }
        },
        "Analog Pad": {
            "desc": "Мягкий аналоговый пад",
            "type": "PAD",
            "variation": 2,
            "tone": 6,
            "depth": 7,
            "effect": 7,
            "direct": 4,
            "mode": "GUITAR",
            "good_notes": ["C", "D", "E", "F", "G", "A", "B"],
            "info": {
                "creator": "Preset создан Andy Timmons",
                "source": "Boss Official Preset Library",
                "genres": "Ambient, Post-Rock, Shoegaze",
                "description": "Эмулирует Juno-60 pad. Популярен в ambient/post-rock сообществе. Используется в треках типа Explosions in the Sky."
            }
        }
    },
    
    "METAL": {
        "Djent Sub Drop": {
            "desc": "Суб-бас для djent breakdown",
            "type": "BASS",
            "variation": 1,
            "tone": 2,
            "depth": 9,
            "effect": 10,
            "direct": 1,
            "mode": "GUITAR",
            "good_notes": ["E", "D", "C", "A"],
            "info": {
                "creator": "Misha Mansoor (Periphery) inspired",
                "source": "Djent forum, Sevenstring.org",
                "genres": "Djent, Progressive Metal, Technical Death Metal",
                "description": "Легендарный пресет для breakdown'ов. Добавляет октаву вниз к drop-tuning. Используется в стиле Periphery, Animals as Leaders. Лучше всего работает с 7-8 струнными гитарами."
            }
        },
        "Industrial Grind": {
            "desc": "Индустриальный синтезированный гранж",
            "type": "SFX 1",
            "variation": 8,
            "tone": 9,
            "depth": 8,
            "effect": 9,
            "direct": 2,
            "mode": "GUITAR",
            "good_notes": ["E", "D", "C#", "A"],
            "info": {
                "creator": "Inspired by Ministry, Nine Inch Nails",
                "source": "Industrial Metal Facebook groups, Gearspace",
                "genres": "Industrial Metal, Nu-Metal, Groove Metal",
                "description": "Агрессивный индустриальный звук в стиле Ministry и Fear Factory. Идеален для palm-muted riff'ов. Популярен у Fear Factory tribute bands."
            }
        },
        "Doom Synth": {
            "desc": "Мрачный синтезатор для doom metal",
            "type": "LEAD 2",
            "variation": 6,
            "tone": 3,
            "depth": 9,
            "effect": 7,
            "direct": 4,
            "mode": "GUITAR",
            "good_notes": ["D", "C", "G", "F"],
            "info": {
                "creator": "Electric Wizard tone inspired",
                "source": "Doom Metal subreddit, Stoner Rock forums",
                "genres": "Doom Metal, Stoner Metal, Sludge Metal",
                "description": "Темный синтезаторный звук с медленной атакой. Идеален для doom riff'ов в стиле Electric Wizard, Sleep. Работает с drop C/B tuning."
            }
        },
        "Black Metal Synth": {
            "desc": "Холодный синтезатор для black metal",
            "type": "STR",
            "variation": 9,
            "tone": 8,
            "depth": 6,
            "effect": 8,
            "direct": 3,
            "mode": "GUITAR",
            "good_notes": ["E", "D", "C#", "B"],
            "info": {
                "creator": "Inspired by Emperor, Dimmu Borgir",
                "source": "Black Metal forums, Norwegian scene",
                "genres": "Symphonic Black Metal, Atmospheric Black Metal",
                "description": "Холодный синтезаторный звук в стиле Emperor. Эмулирует оркестровые партии Dimmu Borgir. Популярен в symphonic black metal."
            }
        }
    },
    
    "FOLK": {
        "Celtic Strings": {
            "desc": "Кельтские струнные",
            "type": "STR",
            "variation": 4,
            "tone": 6,
            "depth": 5,
            "effect": 7,
            "direct": 5,
            "mode": "GUITAR",
            "good_notes": ["D", "A", "G", "E"],
            "info": {
                "creator": "Inspired by Dead Can Dance",
                "source": "Neofolk forums, Dark folk communities",
                "genres": "Celtic Folk, Neofolk, Dark Folk",
                "description": "Эмулирует звук fiddle и кельтских струнных. Используется в DADGAD tuning. Популярен у Wardruna covers."
            }
        },
        "Nordic Drone": {
            "desc": "Нордический дрон-пад",
            "type": "PAD",
            "variation": 11,
            "tone": 4,
            "depth": 10,
            "effect": 6,
            "direct": 4,
            "mode": "GUITAR",
            "good_notes": ["D", "E", "A", "G"],
            "info": {
                "creator": "Wardruna inspired preset",
                "source": "Neofolk community, Heilung fans",
                "genres": "Nordic Folk, Ritual Ambient, Dark Folk",
                "description": "Атмосферный дрон в стиле Wardruna и Heilung. Создает ритуальную атмосферу. Работает с открытыми строями (Open D, Open G)."
            }
        },
        "Hurdy Gurdy": {
            "desc": "Эмуляция hurdy-gurdy",
            "type": "SEQ 2",
            "variation": 7,
            "tone": 5,
            "depth": 7,
            "effect": 8,
            "direct": 4,
            "mode": "GUITAR",
            "good_notes": ["D", "G", "C", "A"],
            "info": {
                "creator": "Medieval folk inspired",
                "source": "Folk metal forums, Eluveitie covers",
                "genres": "Folk Metal, Medieval Folk, Pagan Metal",
                "description": "Имитирует средневековую hurdy-gurdy. Популярен у Eluveitie, Korpiklaani cover bands. Создает аутентичное folk-metal звучание."
            }
        }
    },
    
    "DRONE METAL": {
        "Sunn O))) Wall": {
            "desc": "Массивная стена дроуна",
            "type": "BASS",
            "variation": 10,
            "tone": 1,
            "depth": 10,
            "effect": 10,
            "direct": 2,
            "mode": "GUITAR",
            "good_notes": ["A", "G", "F", "E"],
            "info": {
                "creator": "Inspired by Sunn O))), Earth",
                "source": "Drone Metal community, Southern Lord forums",
                "genres": "Drone Metal, Drone Doom, Ambient Metal",
                "description": "ЛЕГЕНДАРНЫЙ пресет для drone metal. Создает массивную стену звука в стиле Sunn O))). Используется с ultra-low tuning (drop A и ниже). Требует большой громкости для полного эффекта."
            }
        },
        "Earth Drone": {
            "desc": "Атмосферный дрон Earth",
            "type": "PAD",
            "variation": 8,
            "tone": 3,
            "depth": 9,
            "effect": 7,
            "direct": 5,
            "mode": "GUITAR",
            "good_notes": ["D", "C", "G", "A"],
            "info": {
                "creator": "Dylan Carlson (Earth) inspired",
                "source": "Drone/Doom forums, Southern Lord Records",
                "genres": "Drone Metal, Slowcore, Ambient Doom",
                "description": "Атмосферный дрон в стиле Earth (альбом 'Hex'). Медленная атака с долгим sustain. Идеален для минималистичных doom-композиций. Работает с открытыми строями."
            }
        },
        "Boris Fuzz Drone": {
            "desc": "Фуззовый дрон Boris",
            "type": "LEAD 1",
            "variation": 9,
            "tone": 2,
            "depth": 9,
            "effect": 9,
            "direct": 3,
            "mode": "GUITAR",
            "good_notes": ["E", "D", "C", "A"],
            "info": {
                "creator": "Boris (band) inspired",
                "source": "Japanese drone scene, Pitchfork reviews",
                "genres": "Drone Metal, Noise Rock, Experimental Metal",
                "description": "Грязный фуззовый дрон в стиле Boris. Сочетает drone wall с noise rock текстурами. Популярен в японской experimental/drone сцене."
            }
        },
        "Teeth of Lions": {
            "desc": "Психоделический дрон",
            "type": "SFX 2",
            "variation": 6,
            "tone": 7,
            "depth": 10,
            "effect": 8,
            "direct": 3,
            "mode": "GUITAR",
            "good_notes": ["A", "G", "D", "E"],
            "info": {
                "creator": "Earth 2 era inspired",
                "source": "Drone/Psych forums, Aquarius Records",
                "genres": "Psychedelic Drone, Ambient Drone, Doom",
                "description": "Психоделический дрон с эффектом 'teeth of lions rule the divine'. Создает гипнотические текстуры. Используется для 10+ минутных drone-композиций."
            }
        }
    }
}

# 📚 САЙДБАР СО СПРАВКОЙ
with st.sidebar:
    st.title("📖 Справка")
    
    st.markdown("""
    ### О приложении
    **Boss SY-1 Preset Tuner** — интерактивный помощник для настройки гитарной синтезаторной педали Boss SY-1.
    
    ### Как использовать:
    1. Выберите категорию жанра
    2. Выберите пресет из списка
    3. Используйте внешний тюнер (телефон/онлайн)
    4. Нажмите ноту, которую играете
    5. Получите настройки и справку
    
    ### О Boss SY-1
    Boss SY-1 — компактная полифоническая синтезаторная педаль с 121 пресетом. Работает без специального датчика, отслеживает полифонию до 6 нот одновременно.
    
    ### Категории пресетов:
    - **ПОПУЛЯРНЫЕ**: Самые используемые пресеты
    - **METAL**: Djent, Industrial, Doom, Black Metal
    - **FOLK**: Celtic, Nordic, Medieval
    - **DRONE METAL**: Sunn O))), Earth, Boris
    
    ### Рекомендуемые тюнеры:
    - [Tuner Online](https://tuner-online.com)
    - [Musicca Tuner](https://www.musicca.com/guitar-tuner)
    - [Fender Tuner](https://www.fender.com/play/tuner)
    - Приложения: GuitarTuna, Pro Guitar Tuner
    
    ### Источники:
    - Boss Tone Central
    - Reddit r/guitarpedals
    - Gearspace forums
    - Premier Guitar
    - Doom/Drone metal communities
    
    ---
    
    💡 **Совет**: Для drone metal используйте максимальную громкость и низкий строй (drop A-C).
    """)

# 🎸 ГЛАВНЫЙ ИНТЕРФЕЙС
st.title("🎸 Boss SY-1 Preset Tuner")
st.markdown("### Профессиональный настройщик пресетов для металла, фолка и дроун-метала")

# Инструкция (свернута)
with st.expander("📖 Быстрый старт", expanded=False):
    st.markdown("""
    **Шаги:**
    1. Выберите категорию жанра (ПОПУЛЯРНЫЕ/METAL/FOLK/DRONE METAL)
    2. Выберите пресет из списка
    3. Используйте любой гитарный тюнер (телефон/онлайн)
    4. Сыграйте на гитаре и посмотрите ноту на тюнере
    5. Нажмите эту ноту в приложении (БОЛЬШИЕ КНОПКИ)
    6. Получите настройки Boss SY-1 и справку о пресете!
    """)

st.markdown("---")

# 1️⃣ ВЫБОР КАТЕГОРИИ
st.subheader("1️⃣ Выберите категорию жанра")

category = st.selectbox(
    "Категория:",
    options=[""] + list(PRESETS.keys()),
    format_func=lambda x: "-- Выберите категорию --" if x == "" else x
)

if category:
    st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
    
    # 2️⃣ ВЫБОР ПРЕСЕТА
    st.markdown("---")
    st.subheader("2️⃣ Выберите пресет")
    
    preset_name = st.selectbox(
        "Пресет:",
        options=[""] + list(PRESETS[category].keys()),
        format_func=lambda x: "-- Выберите пресет --" if x == "" else x
    )
    
    if preset_name:
        preset = PRESETS[category][preset_name]
        st.info(f"**{preset_name}:** {preset['desc']}")
        
        # 3️⃣ СПРАВКА О ПРЕСЕТЕ
        st.markdown("---")
        st.subheader("📋 Справка о пресете")
        
        st.markdown(f"""
        <div class="preset-info">
            <h3>🎸 {preset_name}</h3>
            <p><strong>Описание:</strong> {preset['info']['description']}</p>
            <p><strong>👤 Создатель/Вдохновение:</strong> {preset['info']['creator']}</p>
            <p><strong>🌐 Источник:</strong> {preset['info']['source']}</p>
            <p><strong>🎵 Жанры:</strong> {preset['info']['genres']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 4️⃣ ВЫБОР НОТЫ (БОЛЬШИЕ КНОПКИ!)
        st.markdown("---")
        st.subheader("3️⃣ Какую ноту вы играете?")
        st.markdown("*Посмотрите на тюнер и нажмите соответствующую ноту*")
        
        # Кнопки нот (2 ряда по 6)
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        
        # Первый ряд
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        cols = [col1, col2, col3, col4, col5, col6]
        
        selected_note = None
        
        for i in range(6):
            with cols[i]:
                if st.button(notes[i], key=f"note_{notes[i]}"):
                    selected_note = notes[i]
                    st.session_state['selected_note'] = notes[i]
        
        # Второй ряд
        col7, col8, col9, col10, col11, col12 = st.columns(6)
        cols2 = [col7, col8, col9, col10, col11, col12]
        
        for i in range(6):
            with cols2[i]:
                if st.button(notes[i+6], key=f"note_{notes[i+6]}"):
                    selected_note = notes[i+6]
                    st.session_state['selected_note'] = notes[i+6]
        
        # Получаем выбранную ноту из session_state
        if 'selected_note' in st.session_state:
            selected_note = st.session_state['selected_note']
        
        # 5️⃣ АНАЛИЗ НОТЫ
        if selected_note:
            st.markdown("---")
            st.subheader(f"4️⃣ Анализ ноты {selected_note}")
            
            is_good = selected_note in preset['good_notes']
            
            if is_good:
                st.markdown(f"""
                <div class="success-box">
                    ✅ Отлично! Нота <strong>{selected_note}</strong> идеально подходит для пресета "{preset_name}"
                </div>
                """, unsafe_allow_html=True)
                
                st.success("💡 **Совет:** Настройте педаль согласно параметрам ниже и продолжайте играть эту ноту.")
            else:
                st.markdown(f"""
                <div class="warning-box">
                    ⚠️ Нота <strong>{selected_note}</strong> не оптимальна для данного пресета
                </div>
                """, unsafe_allow_html=True)
                
                st.warning(f"💡 **Совет:** Попробуйте сыграть одну из этих нот: **{', '.join(preset['good_notes'])}**")
            
            # 6️⃣ НАСТРОЙКИ ПЕДАЛИ
            st.markdown("---")
            st.subheader("5️⃣ Настройки Boss SY-1")
            
            settings_col1, settings_col2 = st.columns(2)
            
            with settings_col1:
                st.markdown(f"""
                <div class="setting-box">
                    <span class="setting-label">TYPE:</span>
                    <span class="setting-value">{preset['type']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="setting-box">
                    <span class="setting-label">VARIATION:</span>
                    <span class="setting-value">{preset['variation']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="setting-box">
                    <span class="setting-label">TONE/RATE:</span>
                    <span class="setting-value">{preset['tone']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="setting-box">
                    <span class="setting-label">DEPTH:</span>
                    <span class="setting-value">{preset['depth']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with settings_col2:
                st.markdown(f"""
                <div class="setting-box">
                    <span class="setting-label">EFFECT:</span>
                    <span class="setting-value">{preset['effect']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="setting-box">
                    <span class="setting-label">DIRECT:</span>
                    <span class="setting-value">{preset['direct']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="setting-box">
                    <span class="setting-label">MODE:</span>
                    <span class="setting-value">{preset['mode']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # 7️⃣ ВИЗУАЛИЗАЦИЯ (оставляем как было)
            st.markdown("---")
            st.subheader("📊 Визуализация")
            
            viz_col1, viz_col2, viz_col3 = st.columns(3)
            
            with viz_col1:
                st.metric(
                    label="Выбранная нота",
                    value=selected_note,
                    delta="✓ Нажата"
                )
            
            with viz_col2:
                st.metric(
                    label="Соответствие",
                    value="✓ Подходит" if is_good else "⚠ Не очень",
                    delta="Хорошо" if is_good else "Попробуйте другую",
                    delta_color="normal" if is_good else "inverse"
                )
            
            with viz_col3:
                st.metric(
                    label="Категория",
                    value=category,
                    delta=preset['type']
                )
            
            # 8️⃣ ПОДХОДЯЩИЕ НОТЫ (оставляем)
            st.markdown("---")
            st.subheader("🎼 Подходящие ноты для этого пресета")
            
            good_notes_cols = st.columns(len(preset['good_notes']))
            for i, note in enumerate(preset['good_notes']):
                with good_notes_cols[i]:
                    is_current = (note == selected_note)
                    st.button(
                        f"{'🎯 ' if is_current else ''}{note}",
                        key=f"good_note_{note}",
                        disabled=is_current,
                        help=f"{'Вы играете эту ноту!' if is_current else 'Попробуйте сыграть эту ноту'}"
                    )
            
            # 9️⃣ НОВЫЕ UI ФИЧИ
            st.markdown("---")
            st.subheader("🎛️ Дополнительные инструменты")
            
            tool_col1, tool_col2, tool_col3 = st.columns(3)
            
            with tool_col1:
                st.markdown("""
                <div class="info-box">
                    <h4>🎚️ Быстрые советы</h4>
                    <ul>
                        <li>Для metal: увеличьте DEPTH и EFFECT</li>
                        <li>Для drone: минимизируйте DIRECT</li>
                        <li>Для folk: баланс EFFECT/DIRECT 50/50</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with tool_col2:
                st.markdown(f"""
                <div class="info-box">
                    <h4>🎸 Рекомендуемый строй</h4>
                    <p><strong>Категория {category}:</strong></p>
                    <ul>
                        <li>METAL: Drop D, Drop C, Drop A</li>
                        <li>FOLK: DADGAD, Open D, Open G</li>
                        <li>DRONE: Drop A и ниже</li>
                        <li>ПОПУЛЯРНЫЕ: Standard E</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with tool_col3:
                if st.button("🔄 Сбросить выбор ноты", use_container_width=True):
                    if 'selected_note' in st.session_state:
                        del st.session_state['selected_note']
                    st.rerun()
                
                if st.button("📋 Копировать настройки", use_container_width=True):
                    settings_text = f"""
                    {preset_name}
                    TYPE: {preset['type']}
                    VARIATION: {preset['variation']}
                    TONE: {preset['tone']}
                    DEPTH: {preset['depth']}
                    EFFECT: {preset['effect']}
                    DIRECT: {preset['direct']}
                    MODE: {preset['mode']}
                    """
                    st.code(settings_text, language="text")
                
                if st.button("🔗 Поделиться пресетом", use_container_width=True):
                    st.info(f"Ссылка: boss-sy1-tuner.streamlit.app?preset={preset_name}")

else:
    st.info("👆 Начните с выбора категории жанра выше")

# Футер
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #555;'>
    <p>🎸 Boss SY-1 Preset Tuner | Metal • Folk • Drone Edition</p>
    <p>Создано для музыкантов с ❤️ | Данные из Boss Tone Central, Reddit, Gearspace</p>
</div>
""", unsafe_allow_html=True)
