module boat_pd_sim_tb;

    logic clk;
    logic rst_n;
    logic signed [31:0] setpoint_x, setpoint_y;
    logic signed [31:0] pos_x, pos_y;
    logic signed [31:0] vel_x, vel_y;
    logic signed [31:0] Kp, Kd;
    logic signed [31:0] control_x, control_y;

    logic signed [31:0] water_current_x, water_current_y;
    int file_handle;
    int time_step;

    boat_pd_sim uut (
        .clk(clk), .rst_n(rst_n),
        .setpoint_x(setpoint_x), .setpoint_y(setpoint_y),
        .pos_x(pos_x), .pos_y(pos_y),
        .vel_x(vel_x), .vel_y(vel_y),
        .Kp(Kp), .Kd(Kd),
        .control_x(control_x), .control_y(control_y)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        file_handle = $fopen("boat_pd_output.csv", "w");
        $fdisplay(file_handle, "Time,SetX,SetY,PosX,PosY,ControlX,ControlY");

        rst_n = 0;
        setpoint_x = 0;
        setpoint_y = 0; 
        pos_x = -500;
        pos_y = -1000;
        vel_x = 0;
        vel_y = 0;
        water_current_x = 30;
        water_current_y = 30;
        time_step = 0;

        Kp = 5;
        Kd = 2;

        #20 rst_n = 1;

        repeat(200) begin
            @(posedge clk);

            setpoint_x = time_step * 10;
            if (time_step < 100)
                setpoint_y = time_step * 10;
            else
                setpoint_y = 1000 - ((time_step - 100) * 10);

            vel_x = vel_x + (control_x / 10) + water_current_x;
            vel_y = vel_y + (control_y / 10) + water_current_y;

            pos_x = pos_x + (vel_x / 10);
            pos_y = pos_y + (vel_y / 10);

            $fdisplay(file_handle, "%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                      time_step, setpoint_x, setpoint_y, pos_x, pos_y, control_x, control_y);
            time_step++;

            if (time_step == 120) begin
                water_current_x = -50;
                water_current_y = 80;
            end
        end

        $fclose(file_handle);
        $display("Simulation complete. Data written to boat_pd_output.csv");
        $finish;
    end
endmodule
