function [sock_signals,body_signals,sock_logical,body_logical] = load_data(file_dir,signal_type)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% LOAD_DATA loads the data from the specified structure and returns the matrix containing the data
% Inputs:
%   - file_dir: path to the MAT file
%   - signal_type: (str) name of the signal types to be loaded from
%               [AvgBeatVe,singleBeatVe,rawVe]
% Returns:
%   - sock_signals_cell: [num_ECGs x num_samples] signals from the heart
%   - body_signals_cell: [num_ECGs x num_samples] signals from the body
%   - sock_logical: [1 x num_ECGs] position of bad leads in sock signals
%   - body_logical: [1 x num_ECGs] position of bad leads in body signals
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

signals = load(file_dir);
fprintf("Loading data from %s with signal type %s \n",file_dir,signal_type);
if isequal(signal_type,'AvgBeatVe')
    sock_signals = signals.Signals.sock.AvgBeatVe;
    body_signals = signals.Signals.torso.AvgBeatVe;
elseif isequal(signal_type,'singleBeatVe')
    sock_signals = signals.Signals.sock.singleBeatVe;
    body_signals = signals.Signals.torso.singleBeatRaw;
else
    sock_signals = signals.Signals.sock.rawVe;
    body_signals = signals.Signals.torso.rawVe;
end 
sock_logical = signals.Signals.sock.badLeads;
body_logical = signals.Signals.torso.badLeads;




