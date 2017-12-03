var healtharray = ["Give your yogurt or smoothie a healthy boost with a couple of teaspoons of flaxseed oil.","Add garlic to your diet. It to spieces up the taste, <br />but also improves your circulatory system and overall wellbeing.","Eating breakfast on a daily basis does not need to be time consuming. <br />Plan ahead and fill your breakfast with healthy option, such as fruit.","Keep a food journal and write down everything you eat. <br />This is one of the best methods to control your weight.","A single cup of green tea every day can help reduce the risk of heart disease and cancer.",'If you take medicine regularly, why not mark it on your calendars and "to do" lists, <br />so you never forget and form a solid habit.',"When board, anxious of lonely, engage in some sort of physical activity. <br />Exercise can help your mind get out of its doldrums.","Coconut oil can act as a skin moisturizer and lip balm.","Dilute juice with sparkling water to cut calories and to act as a bubbly soda replacement.","Add sources of fiber, such as a whole grains, to your diet to improve health.",'Immediately after grocery shopping, wash and prepare fruits and vegetables:<br /> making them easier to consume "on-the-go".']		// Array of healthtips
var healthrandom = healtharray[Math.floor(Math.random() * healtharray.length)]		//Randomly choose 1 out of the total number of strings in the array

$(document).ready(function () {
    $('body').append('<div><div class="row"><div id="healthdiv" class="col-sm-4 fadeintopage closehealth"><h4>Health Tip</h4><p><span id="healthtips"></span><br /><strong>Click this dialog to close it</strong></p></div></div></div></div>');		// Appends the healthtip at the bottom of the page
	$('#healthtips').html(healthrandom);
	$('.closehealth').click(function(){
		$(this).fadeOut(200, function() {
		$(this).remove();
		});
	});
});
