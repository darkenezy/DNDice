$(".addDiceButton").click(function(){
    dice_desc = $(this).attr("id")
    $.ajax({
        type: "POST",
        url: "/api/v1/add_dice",
        contentType: 'application/json',
        data: JSON.stringify({dice_desc: dice_desc}),
        success: function(data) {
            $("#counter").text("?");
            drawDice(data);
        }

    });
});

$("#rollButton").click(function(){
    if($('.dice').length==0) {
        return;
    }
    $(".roll").fadeOut(150);
    $({deg: 0}).animate({deg: 270}, {
        duration: 300,
        step: function(now) {
            $(".dice").css({
                transform: 'rotate(' + now + 'deg)'
            });
        },
        complete: function(){
             $.ajax({
                type: "POST",
                url: "/api/v1/roll",
                success: refreshDice
            });
        }
    });
});

$("#clearAllButton").click(function(){
    if($('.diceContainer').length==0) {
        return;
    }
    $(".diceContainer").fadeOut(150);

    setTimeout(function() {
        $.ajax({
            type: "DELETE",
            url: "/api/v1/remove_dice/all",
            success: function() {
                $("#counter").text("?");
            },
            error: function() {
                $(".diceContainer").show();
            }
        });
    }, 150);
});

function drawDice(data, hide_roll=false) {
    dice_id = data.dice_id
    dice_desc = data.dice_desc
    color = data.color
    value = data.value

    // Preparing parts
    let container = $('<div class="diceContainer"></div>');
    let dice = $('<div class="dice"></div>');
    let roll = $('<label class="roll">' + value + '</label>');
    let type = $('<label class="type">' + dice_desc + '</label>');

    // Set up dice
    dice.attr("id", dice_id)
    dice.css("background-color", color);

    // Reusing code in refreshDice
    if (hide_roll) {
        roll.hide();
    }

    // Making up the sandwich
    container.append(dice.append(roll)).append(type);

    // Append it to canvas
    $(".canvas").append(container);
    return value;
}
function refreshDice() {
    $.get("/api/v1/get_dice").done(function(data){
        $(".canvas").empty();
        let total = 0;

        for (let id in data) {
            value = drawDice(data[id], hide_roll=true);
            if(total != "?") {
                if(value != "?") {
                    total += value;
                }
                else {
                    total = "?";
                }
            }
        }
        $(".roll").fadeIn(150, function(){ $("#counter").text(total); });

    })
}

$(".canvas").on('click', ".dice", function(event){
    let dice = $(this)
    let parent = dice.parent()
    $.ajax({
        type: "DELETE",
        url: "/api/v1/remove_dice/" + dice.attr("id"),
        success: function() { parent.fadeOut(150, function() { parent.remove() }) }
    });
});

$(document).ready(refreshDice);






