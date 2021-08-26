(
var gui, sliders, sliderNum, values, sliderLayout, netAddr;

var sliderNames = ['/slider0', '/slider1', '/slider2', '/slider3'];

netAddr = NetAddr("127.0.0.1", 57121);

gui = Window("servoCom", Rect(200, 400, 400, 200))
.background_(Color.black).front;

sliderNum = 4;

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

