module boat_pd_sim (
    input  logic clk,
    input  logic rst_n,
    input  logic signed [31:0] setpoint_x,
    input  logic signed [31:0] setpoint_y,
    input  logic signed [31:0] pos_x,
    input  logic signed [31:0] pos_y,
    input  logic signed [31:0] vel_x,
    input  logic signed [31:0] vel_y,
    input  logic signed [31:0] Kp,
    input  logic signed [31:0] Kd,
    output logic signed [31:0] control_x,
    output logic signed [31:0] control_y
);

    logic signed [31:0] error_x;
    logic signed [31:0] error_y;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            control_x <= 0;
            control_y <= 0;
        end else begin
            error_x = setpoint_x - pos_x;
            error_y = setpoint_y - pos_y;
            
            control_x <= (Kp * error_x) - (Kd * vel_x);
            control_y <= (Kp * error_y) - (Kd * vel_y);
        end
    end
endmodule
