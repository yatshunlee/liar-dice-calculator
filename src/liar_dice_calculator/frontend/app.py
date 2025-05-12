import streamlit as st
from liar_dice_calculator.core import LiarDiceCalculator
from liar_dice_calculator.visualization import plot_heatmap

calculator = LiarDiceCalculator()

def main():
    st.title("Liar Dice Calculator 大話骰計算器")

    n_players = st.number_input(
        "Number of players 幾多玩家 (including yourself 計埋自己)", min_value=2, max_value=10, value=2, step=1
    )

    st.write("Input your combination of 5 dice 輸入5顆骰子嘅面值")

    dice_face_values = {
        i + 1: "⚀⚁⚂⚃⚄⚅"[i]for i in range(6)
    }
    
    player_dice_in_lst = []
    player_dice = {}
    cols = st.columns(5)
    for i in range(5):
        dice_val = cols[i].number_input(
            label=f"Die 骰子 {i+1}",
            min_value=1, max_value=6, value=1, step=1, key=f"dice_{i}"
        )
        player_dice.setdefault(dice_val, 0)
        player_dice[dice_val] += 1
        player_dice_in_lst.append(dice_val)
    
    is_wild = st.radio(
        "Select an option 選擇以下一個選項:",
        ["Wild 1 走齌", "Not Wild 齌"],
        horizontal=True
    )
    is_wild = True if is_wild == "Wild 1 走齌" else False

    degree_of_belief = st.slider(
        "Degree of belief 上手可信度 (0 possibly lying 唔係好信 - 2 honest guy aka 老實人)", min_value=0, max_value=2, value=0, step=1
    )

    if st.button("Generate Prediction 生成預測"):
        st.success("Generated prediction successfully 成功生成預測")
        hmap = calculator.predict(n_players, is_wild, player_dice, degree_of_belief)
        fig, _ = plot_heatmap(hmap)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
