// GUI for controlling text output and actuator positions
(
var sliders, sliderNum, values, sliderLayout, netAddr;
var dataPath, lines, wordDict, now, curWord, keyWords, str, sentence, gui, btn, randBtn, killBtn, newTextBtn, textField, nextWord, dropdown, pidList;
var textDelay, sliderDelay;
var textDelayVal, sliderDelayVal;
var sliderBtn;
var sliderNames = ['/slider0', '/slider1', '/slider2', '/slider3', '/slider4'];
var slidersActivated = true;

keyWords = ["body", "gender", "cyborg"];

netAddr = NetAddr("127.0.0.1", 57121);

sliderNum = sliderNames.size;

textDelayVal = 0;
sliderDelayVal = 0;

textDelay = Slider().orientation_(\horizontal);
sliderDelay = Slider().orientation_(\horizontal);

textDelay.action_({ |slider|
	var val;
	val = slider.value;
	textDelayVal = val.linlin(0, 1, 0, 3);
	("text delay value: " + textDelayVal).postln;
});

sliderDelay.action_({ |slider|
	var val;
	val = slider.value;
	sliderDelayVal = val.linlin(0, 1, 0, 3);
	("slider delay value: " + sliderDelayVal).postln;
});

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

sliderBtn = Button()
.states_([
	["Sliders Activated", Color.black, Color.white],
	["Sliders Deactivated", Color.white, Color.black]
])
.action_({
	slidersActivated = slidersActivated.not;
	postln("sliders activated: " + slidersActivated)
});


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
	var curWord, curSentence, str, randNum;
	curWord = dropdown.item;
	randNum = [1, 2, 3].choose;
	str = "";
	randNum.do({
		var thisSentence;
		thisSentence = "";
		curSentence = wordDict[curWord].choose;
		curSentence.do({ |word|
			thisSentence = thisSentence + " " + word;
		});
		thisSentence = thisSentence.stripWhiteSpace() + " ";
		str = str + thisSentence;
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
	fork {
		{
			if (slidersActivated, {
				sliders.do({ |slider, i|
					var val = slider.value.linlin(0, 1, 45, 160).asInt;
					val.postln;
					netAddr.sendMsg(sliderNames[i], val)
				});
			});
		}.defer(sliderDelayVal);
		{
			pidList = pidList ++ ("say" + textField.string).unixCmd;
		}.defer(textDelayVal);
	}.defer
});

gui.layout_(
	VLayout(
		HLayout(
			VLayout(
				randBtn,
				HLayout(*sliderLayout),
				sliderBtn,
				sliderDelay,
			),
			VLayout(
				textField,
				dropdown,
				newTextBtn,
				killBtn,
				textDelay
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

ServerOptions.devices

s.options.device_("Built-in Output")



