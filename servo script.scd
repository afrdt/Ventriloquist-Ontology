// GUI for controlling text output and actuator positions
(
var sliders, sliderNum, values, sliderLayout, netAddr;
var dataPath, lines, wordDict, now, curWord, keyWords, str, sentence, gui, btn, randBtn, killBtn, newTextBtn, textField, nextWord, dropdown, pidList;
var sliderNames = ['/slider0', '/slider1', '/slider2', '/slider3', '/slider4'];

keyWords = ["body", "gender", "cyborg"];

netAddr = NetAddr("127.0.0.1", 57121);

sliderNum = sliderNames.size;

pidList = [];
values = sliderNum.collect({ |i|
	StaticText()
	.stringColor_(Color.white)
});

sliders = sliderNum.collect({ |i|
	Slider()
	.orientation_(\vertical)
	.action_({ |slider|
	})
});

sliderLayout = sliders.collect({ |slider, i|
	VLayout(
		sliders[i],
		StaticText()
		.string_("Slider" ++ i)
		.stringColor_(Color.white)
		.align_(\center)
	)
});


gui = Window("VO", Rect(200, 200, 550, 400), false)
.front
.background_(Color.black);

dataPath = PathName("".resolveRelative +/+ "data");
wordDict = Dictionary.new();


randBtn = Button()
.states_([
	["Randomize Sliders", Color.black, Color.white]
])
.action_({
	sliders.do({|slider|
		slider.valueAction_(rrand(0.0, 1.0))
	})
});

keyWords.do({ |thisKey|
	wordDict.put(thisKey, Set.new())
});

killBtn = Button()
.states_([
	["Kill Voice", Color.black, Color.white]
])
.action_({
	pidList.do({ |pid|
		("kill" + pid).unixCmd
	})
});

dataPath.entries.do({|thisEntry|
	var file;

	file = FileReader.new(thisEntry.fullPath, true);

	file.do({|thisLine|
		thisLine.do({|thisWord|
			if (wordDict.keys.includes(thisWord), {
				wordDict[thisWord].add(thisLine);
			})
		})
	})
});

now = 0;
curWord = wordDict.keys.asArray.choose;
str = "";
wordDict[curWord].choose;

textField = TextView().minWidth_(150).minHeight_(200).string_("");

dropdown = PopUpMenu().items_(keyWords);

newTextBtn = Button()
.states_([
	["New Text", Color.black, Color.white]
])
.action_({
	var curWord, curSentence, str;
	curWord = dropdown.item;
	curSentence = wordDict[curWord].choose;
	str = "";
	curSentence.do({ |word|
		str = str + " " + word;
	});
	str = str.stripWhiteSpace();
	textField.string_(str)
	// ("say " + str).unixCmd;
});

newTextBtn.valueAction_(0);

dropdown.action_({
	newTextBtn.valueAction_(0);
});


btn = Button()
.states_([
	["Execute", Color.black, Color.white]
])
.minHeight_(50)
.action_({ |btn|
	sliders.do({ |slider, i|
		var val = slider.value.linlin(0, 1, 0, 180).asInt;
		val.postln;
		netAddr.sendMsg(sliderNames[i], val)
	});
	pidList = pidList ++ ("say" + textField.string).unixCmd;
});

gui.layout_(
	VLayout(
		HLayout(
			VLayout(
				randBtn,
				HLayout(*sliderLayout),
			),
			VLayout(
				textField,
				dropdown,
				newTextBtn,
				killBtn
			),
		),
		btn
	)
);
)


// GUI to move actuators in real time
(
var gui, sliders, sliderNum, values, sliderLayout, netAddr;
var sliderNames = ['/slider0', '/slider1', '/slider2', '/slider3', '/slider4'];

netAddr = NetAddr("127.0.0.1", 57121);

gui = Window("servoCom", Rect(200, 400, 400, 200))
.background_(Color.black).front;

sliderNum = sliderNames.size;

values = sliderNum.collect({ |i|
	StaticText()
	.stringColor_(Color.white)
});

sliders = sliderNum.collect({ |i|
	Slider()
	.orientation_(\vertical)
	.action_({ |slider|
		var val;
		val = slider.value.linlin(0, 1, 0, 180);
		val.asInt.postln;
		netAddr.sendMsg(sliderNames[i], val.asInt)
	})
});

sliderLayout = sliders.collect({ |slider, i|
	VLayout(
		sliders[i],
		StaticText()
		.string_("Slider " + i)
		.stringColor_(Color.white)
		.align_(\center)
	)
});

gui.layout_(
	HLayout(*sliderLayout)
)

)

b = NetAddr.localAddr
b = NetAddr("127.0.0.1", 57121)
(
OSCdef(\test, { |...args|
	args.postln;

}, '/fred')
)
b.sendMsg('/fred', 60)

b.sendMsg(10)

