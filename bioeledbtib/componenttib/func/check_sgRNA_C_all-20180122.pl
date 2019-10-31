#!/usr/bin/perl
$fi="report_protospacer.txt";
$fo="report_protospacer_out.txt";

open FI, "$fi" or die "can't open file in\n";
open FO, ">$fo" or die "can't open file out\n";

while(<FI>){
	chomp;
	my @str=split/\t/;
	my @length=$str[0];
	my @length=split/-/;
	print FO "$_";
	if ($str[0]=~ m/(_S_)/g){
		my $seq=substr($str[3],0,7);   #提取7位字符串，即可编辑区
		while ($seq=~ m/(CAA)/g) {
			my $end=pos($seq);          #判断CAA在可编辑区的位置，给出的是A的位置，不是C的
			my $ss=($str[1]+$end-4)%3;   #结合sgRNA起始位置和CAA在可编辑区的位置，判断C是否可编辑
			if($ss==0){
				my $ll=$end-2;
				my $per=($str[1]+$end-3)*100/$length[1];
				print FO "\tCAA\t1\t$ll\t$per";
			}
			else{
				print FO "\tCAA\t0\t-\t-";
			}
		}
		while ($seq=~ m/(CGA)/g) {
			my $end=pos($seq);
			my $ss=($str[1]+$end-4)%3;
			if($ss==0){
				my $ll=$end-2;
				my $per=($str[1]+$end-3)*100/$length[1];
				print FO "\tCGA\t1\t$ll\t$per";
			}
			else{
				print FO "\tCGA\t0\t-\t-";
			}
		}
		while ($seq=~ m/(CAG)/g) {
			my $end=pos($seq);
			my $ss=($str[1]+$end-4)%3;
			if($ss==0){
				my $ll=$end-2;
				my $per=($str[1]+$end-3)*100/$length[1];
				print FO "\tCAG\t1\t$ll\t$per";
			}
			else{
				print FO "\tCAG\t0\t-\t-";
			}
		}
		print FO "\n";
	}
	else{
		my $seq=substr($str[3],0,7);
		while ($seq=~ m/(CCA)/g) {
			my $end=pos($seq);
			my $ss=($str[2]-$end)%3;     #anti-sense时，根据sgRNA终止位置，CCA在可编辑区的位置（A在可编辑区的位置），整合判断C是可编辑
			if($ss==0){
				my $ll=$end-2;
				my $per=($str[2]-$end+3)*100/$length[1];
				print FO "\tCCA\t1\t$ll\t$per";
			}
			else{
				print FO "\tCCA\t0\t-\t-";
			}
		}
			print FO "\n";
	}
		
}
close FI;
close FO;