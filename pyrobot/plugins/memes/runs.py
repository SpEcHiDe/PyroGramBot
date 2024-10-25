import random
from pyrogram import Client, filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter


RUN_STRINGS = [
    "ഇരുട്ട് നിറഞ്ഞ എന്റെ ഈ ജീവിതത്തിലേക്ക് ഒരു തകർച്ചയെ \
    ഓർമ്മിപ്പിക്കാൻ എന്തിന് ഈ ഓട്ടക്കാലണ ആയി നീ വന്നു",
    "നമ്മൾ നമ്മൾ പോലുമറിയാതെ അധോലോകം ആയി മാറിക്കഴിഞ്ഞിരിക്കുന്നു ഷാജിയേട്ടാ...",
    "എന്നെ ചീത്ത വിളിക്കു... വേണമെങ്കിൽ നല്ല ഇടി ഇടിക്കു... പക്ഷെ ഉപദേശിക്കരുത്.....",
    "ഓ ബ്ലഡി ഗ്രാമവാസീസ്!",
    "സീ മാഗ്ഗി ഐ ആം ഗോയിങ് ടു പേ ദി ബിൽ.",
    "പോരുന്നോ എന്റെ കൂടെ!",
    "തള്ളെ കലിപ്പ് തീരണില്ലല്ലോ!!",
    "ശബരിമല ശാസ്താവാണെ ഹരിഹരസുതനാണെ ഇത് ചെയ്തവനെ ഞാൻ പൂട്ടും നല്ല മണിച്ചിത്രത്താഴിട്ട് പൂട്ടും .",
    "ഞാൻ കണ്ടു...!! കിണ്ടി... കിണ്ടി...!",
    "മോന്തയ്ക്കിട്ട് കൊടുത്തിട്ട് ഒന്ന് എടുത്ത് കാണിച്ചുകൊടുക്ക് അപ്പോൾ കാണും ISI മാർക്ക് ",
    "ഡേവീസേട്ട, കിങ്ഫിഷറിണ്ടാ... ചിൽഡ്...! .",
    "പാതിരാത്രിക്ക് നിന്റെ അച്ഛൻ ഉണ്ടാക്കി വെച്ചിരിക്കുന്നോ പൊറോട്ടയും ചിക്കനും....",
    "ഇത് ഞങ്ങളുടെ പണിസാധനങ്ങളാ രാജാവേ.",
    "കളിക്കല്ലേ കളിച്ചാൽ ഞാൻ തീറ്റിക്കുമെ പുളിമാങ്ങ....",
    "മ്മക്ക് ഓരോ ബിയറാ കാച്ചിയാലോ...",
    "ഓ പിന്നെ നീ ഒക്കെ പ്രേമിക്കുമ്പോൾ അത് പ്രണയം.... നമ്മൾ ഒക്കെ പ്രേമിക്കുമ്പോൾ അത് കമ്പി...",
    "കള്ളടിക്കുന്നവനല്ലേ കരിമീനിന്റെ സ്വാദറിയു.....",
    "ഡാ വിജയാ നമുക്കെന്താ ഈ ബുദ്ധി നേരത്തെ തോന്നാതിരുന്നത്...!",
    "ഇത്രേം കാലം എവിടെ ആയിരുന്നു....!",
    "ദൈവമേ എന്നെ മാത്രം രക്ഷിക്കണേ....",
    "എനിക്കറിയാം ഇവന്റെ അച്ഛന്റെ പേര് ഭവാനിയമ്മ എന്നാ....",
    "ഡാ ദാസാ... ഏതാ ഈ അലവലാതി.....",
    "ഉപ്പുമാവിന്റെ ഇംഗ്ലീഷ് സാൾട് മംഗോ ട്രീ.....",
    "മക്കളെ.. രാജസ്ഥാൻ മരുഭൂമിയിലേക്ക് മണല് കയറ്റിവിടാൻ നോക്കല്ലേ.....",
    "നിന്റെ അച്ഛനാടാ പോൾ ബാർബർ....",
    "കാർ എൻജിൻ ഔട്ട് കംപ്ലീറ്റ്‌ലി.....",
    "ഇത് കണ്ണോ അതോ കാന്തമോ...",
    "നാലാമത്തെ പെഗ്ഗിൽ ഐസ്‌ക്യൂബ്സ് വീഴുന്നതിനു മുൻപ് ഞാൻ അവിടെ എത്തും.....",
    "അവളെ ഓർത്ത് കുടിച്ച കല്ലും നനഞ്ഞ മഴയും വേസ്റ്റ്....",
    "എന്നോട് പറ ഐ ലവ് യൂ ന്ന്....",
    "അല്ല ഇതാര് വാര്യംപിള്ളിയിലെ മീനാക്ഷി അല്ലയോ... എന്താ മോളെ സ്കൂട്ടറില്.... ",
    # Shonen
    'Why did the Shonen hero cross the road? To train on the other side! 💪⚔️🚶‍♂️',
    'How do Shonen heroes make friends? By saving the world, of course! 🌍❤️💪',
    'Why don’t Shonen heroes use elevators? They prefer to take the stairs to greatness! 🏆🚶‍♂️✨',
    'What’s a Shonen hero’s favorite type of music? Anything with a good training montage! 🎶💪📈',
    # Shojo
    'What did the Shojo girl say on her date? "I’m falling for you, just like in the manga!" 💕🌹📚',
    'Why did the Shojo character blush? Because her favorite romance anime just got a season two! 😳❤️🎬',
    'How do Shojo characters stay cool? They have a fan club! 🎐💖🌸',
    'What’s a Shojo character’s favorite exercise? Heart skips! ❤️💓💪',
    # Isekai
    'Why did the Isekai protagonist get a job? To make a name in another world! ✨🌍💼',
    'What’s an Isekai hero’s favorite hobby? Exploring new dimensions! 🗺️🔮🌌',
    'Why don’t Isekai heroes need maps? They always find their way to adventure! 🌟🗺️🚀',
    'What do you call an Isekai hero who loves cooking? A master of dimension cuisine! 🍲🔮🌟',
    # Mecha
    'Why did the Mecha pilot go to therapy? To work through his robot issues! 🤖💔🛠️',
    'What’s a Mecha pilot’s favorite drink? Mega-sized cola! 🥤🤖🚀',
    'How do Mecha robots stay in shape? With a lot of heavy lifting! 🤖💪🏋️‍♂️',
    'What’s a Mecha’s favorite pastime? Power moves and epic battles! ⚔️🤖💥',
    # Sports
    'Why did the sports anime character get kicked out of the gym? Too many dramatic moments! 🏋️‍♂️🎭😂',
    'What’s a sports anime fan’s favorite snack? Energy bars and victory cheers! 🏅🍫🎉',
    'How do sports anime characters stay focused? They always have their game face on! 😎🏆⚽',
    'Why did the sports anime star bring a ladder to the game? To reach new heights! 🏀🚀🏆',
    # Horror
    'Why don’t horror anime characters use elevators? They’re afraid of unexpected scares! 🕯️😱🚪',
    'What’s a horror anime character’s favorite dessert? Scary-sweet treats! 🍰👻💀',
    'How do horror anime characters stay calm? By telling themselves it’s just fiction! 📚😅👻',
    'Why did the horror anime protagonist go to the therapist? Too many nightmares! 😨🛏️🔮',
    # Slice of Life
    'Why did the Slice of Life character bring an umbrella? To be prepared for all life’s showers! ☔🏠🌦️',
    'What’s a Slice of Life character’s favorite hobby? Collecting everyday moments! 📚✨☕',
    'How do Slice of Life characters stay organized? With lots of cute planners! 📅🎀✏️',
    'Why did the Slice of Life character adopt a pet? To add a little more cuteness to their routine! 🐾💖📅',
    # Mystery
    'Why did the detective in the mystery anime bring a pencil? To draw his conclusions! ✏️🔍🕵️‍♂️',
    'What’s a mystery anime character’s favorite drink? Clue-ade! 🍹🔎🕵️‍♀️',
    'How do mystery anime characters solve crimes? By piecing together the plot! 🧩🔍📜',
    'Why was the mystery anime character always calm? They always had the answers! 😎🕵️‍♂️📚',
    # Fantasy
    'Why did the fantasy character get a pet dragon? For a fiery sidekick! 🐉🔥👯',
    'What’s a fantasy hero’s favorite tool? A wand with endless possibilities! 🪄✨🔮',
    'How do fantasy characters relax? By reading ancient scrolls! 📜🌟💤',
    'Why did the wizard visit the library? To find magical reads! 📚✨🧙',
    # Romance
    'Why did the romance anime couple go to the park? For some heart-to-heart conversations! 🌹💬🌳',
    'What’s a romance anime character’s favorite pickup line? "Are you a magic spell? Because you make my heart flutter!" 💕✨🧙‍♂️',
    'Why did the romance anime character bring a ladder? To reach new heights in love! 💖🚀🌹',
    'How do romance anime characters keep their relationships fresh? With regular sweet gestures! 💌🌟🍫',
    # Comedy
    'Why did the comedy anime character go to the bank? To make a deposit of laughs! 😂🏦💰',
    'What’s a comedy anime character’s favorite snack? Chuckle chips! 😂🍟😋',
    'How do comedy anime characters stay upbeat? They always find the punchline! 😂🔍✨',
    'Why did the comedy anime star cross the road? To get to the joke side! 😂🚶‍♂️🎭',
    # Drama
    'Why did the drama anime character start a blog? To share their emotional outbursts! 😭💻📝',
    'What’s a drama anime character’s favorite drink? Tears and tension tea! 😢☕🔥',
    'How do drama anime characters keep their cool? By practicing their emotional monologues! 🎭😌🗣️',
    'Why did the drama anime character carry a diary? To pen down every dramatic moment! 📖🎭✨',
    # Sci-Fi
    'Why did the sci-fi hero bring a spaceship to the party? To add some futuristic fun! 🚀🎉🪐',
    'What’s a sci-fi fan’s favorite accessory? Holographic sunglasses! 🕶️🌌✨',
    'How do sci-fi characters keep track of time? With a personal space-time calculator! ⏳🔭🚀',
    'Why did the sci-fi character visit the moon? To have a stellar weekend! 🌕🚀🎉',
    # Historical
    'Why did the historical anime character visit the museum? To relive the epic battles! 🏛️⚔️🛡️',
    'What’s a historical anime fan’s favorite hobby? Re-enacting classic scenes! 🎭🏰🔍',
    'How do historical anime characters stay in shape? With ancient martial arts! 🥋🏹🏆',
    'Why did the historical figure start a band? To revive some classic tunes! 🎸🎻📜',
    # Supernatural
    'Why don’t supernatural characters play hide and seek? They’re always found out by their auras! 🌟👻🔮',
    'What’s a supernatural being’s favorite game? Spirit tag! 👻🏃‍♂️💨',
    'How do supernatural characters stay fit? By floating through their daily workout! ✨🧘‍♂️🌙',
    'Why did the supernatural character get a pet? To add some magic to their life! 🐾✨🔮',
    # Action
    'Why did the action star bring a parachute? For some high-flying stunts! 🪂💥🚀',
    'What’s an action hero’s favorite type of music? Anything with a fast beat! 🎶🔥🏆',
    'How do action stars stay fit? By practicing their fight scenes! 🥋💪⚔️',
    'Why did the action hero carry a map? To plan his next big adventure! 🗺️🚀🔥',
    # Adventure
    'Why did the adventurer bring a compass? To find their way to excitement! 🧭🌍🚀',
    'What’s an adventurer’s favorite snack? Trail mix and treasure treats! 🏞️🍫💎',
    'How do adventurers stay motivated? By dreaming of epic quests! 🗺️✨🏆',
    'Why did the adventurer climb the mountain? To see the view from the top of the world! 🏔️🌟👀',
    # Music
    'Why did the music anime character join a band? To hit the high notes! 🎸🎶🌟',
    'What’s a musician’s favorite anime? One with a lot of musical battles! 🎤🎻🎹',
    'How do music characters stay in tune? By practicing their scales every day! 🎵🎸📈',
    'Why did the music anime character write a song? To compose their feelings! 🎶❤️📝',
    # Psychological
    'Why did the psychological anime character see a therapist? To unravel their mind’s mysteries! 🧠🛋️🔍',
    'What’s a psychological anime fan’s favorite activity? Analyzing character motivations! 🤔📚🔍',
    'How do psychological anime characters handle stress? By overthinking everything! 😅🧠📈',
    'Why did the psychological anime character start a journal? To document their inner chaos! 📓🧠💭',
]


@Client.on_message(filters.command("runs", COMMAND_HAND_LER) & f_onw_fliter)
async def runs(_, message):
    """ /runs strings """
    effective_string = random.choice(RUN_STRINGS)
    if message.reply_to_message:
        await message.reply_to_message.reply_text(effective_string)
    else:
        await message.reply_text(effective_string)
