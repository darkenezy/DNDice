$(".addDiceButton").click(function(){
    dice_desc = $(this).attr("id")
    dice_id = Math.floor(Math.random()*16777215).toString(16)
    $.ajax({
        type: "POST",
        url: "/api/v1/add_dice",
        contentType: 'application/json',
        data: JSON.stringify({dice_id: dice_id, dice_desc: dice_desc}),
        success: refreshDice,
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
    $(".diceContainer").fadeOut(150, function() {
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
    });
});

function refreshDice() {
    $.get("/api/v1/get_dice").done(function(data){
        $(".canvas").empty();
        let total = 0;

        for (let dice_id in data) {
            color = data[dice_id]["color"]
            dice_desc = data[dice_id]["desc"]
            value = data[dice_id]["value"]

            if(total != "?") {
                if(value != "?") {
                    total += value;
                }
                else {
                    total = "?";
                }
            }

            // Create dice element
            let container = $('<div class="diceContainer"></div>');
            let dice = $('<div class="dice"></div>');
            let roll = $('<label class="roll">' + value + '</label>');
            let type = $('<label class="type">' + dice_desc + '</label>');

            roll.hide();
            dice.css("background-color", color);
            container.append(dice.append(roll)).append(type);

            dice.on("click", function(){
                $.ajax({
                    type: "DELETE",
                    url: "/api/v1/remove_dice/" + dice_id,
                    success: function() { container.fadeOut() }
                });
            });

            // Append it to canvas
            $(".canvas").append(container);
        }
        $(".roll").fadeIn(150, function(){ $("#counter").text(total); });

    })
}

$(document).ready(refreshDice);






