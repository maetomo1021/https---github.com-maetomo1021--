{
    {
        Random random = new Random();
        int target = random.nextInt(10);
        int count = 0;
        int guess;
        System.out.println("数あてゲーム");
        do {
            System.out.print("0～9の数値を入力してください：");
            guess = Integer.parseInt(reader.readLine());
            count++;
        } while (guess != target);
        System.out.println("正解！");
        System.out.println("試行回数：" + count + "回！");

        //op2
        int total = 0;
        while (true) {
            System.out.println("単価と数量を入力してください。終了するは単価に-1を入力してください。");
            System.out.print("単価：");
            int price = Integer.parseInt(reader.readLine());
            if (price == -1) {
                break;
            }
            System.out.print("数量：");
            int quantity = Integer.parseInt(reader.readLine());
            total += price * quantity;
        }
        int tax = (int) (total * 1.1);
        System.out.println("合計金額：" + total);
        System.out.println("税込金額：" + tax);
    }
}