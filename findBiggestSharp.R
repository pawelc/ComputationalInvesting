# TODO: Add comment
# 
# Author: pawelc
###############################################################################

library(PerformanceAnalytics)
library(zoo)
library(tseries)

TRADING_DAYS_IN_YEAR=252

allTickers.df = read.csv(file="http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
		stringsAsFactors=FALSE)
all.r.daily = NULL
ignored=0
for(i in 1:nrow(allTickers.df)){
	sym = allTickers.df$Symbol[i]
	print(sprintf("getting sym %s %d/%d",sym,i,dim(allTickers.df)[1]))
	result = tryCatch({
				prices.daily = get.hist.quote(instrument=sym, start="2011-01-01",
						end="2011-12-31", quote="AdjClose",
						provider="yahoo", origin="1970-01-01",
						compression="d", retclass="ts",quiet = TRUE)
			}, warning = function(w) {
				print(sprintf("warning: %s",w))
			}, error = function(e) {
				print(sprintf("error: %s",e))
				ignored=ignored+1
				next
			})
	
	prices.daily = na.remove(prices.daily)
	prices.count=nrow(prices.daily)
	if(prices.count!=TRADING_DAYS_IN_YEAR){
		print(sprintf("ignoring %s because valid prices: %d",sym,prices.count))
		ignored=ignored+1
		next
	}
	r.daily = prices.daily[-1]/prices.daily[-length(prices.daily)]-1
	if(is.null(all.r.daily)){
		all.r.daily=matrix(r.daily)	
	}else{		
		all.r.daily = cbind(all.r.daily,matrix(r.daily))
	}
	colnames(all.r.daily)[ncol(all.r.daily)]=sym
}

print(sprintf("Ignored: %d",ignored))

load("rDailyNasdaq.Rda")
mu.r.daily=apply(all.r.daily,2,mean)
sigma.r.daily=apply(all.r.daily,2,sd)
instruments.sharp.ratios=sort(sqrt(TRADING_DAYS_IN_YEAR)*mu.r.daily/sigma.r.daily,decreasing = TRUE)

#build portfolio out of biggest ratios
instrument.count=4
combinations=combn(1:60,4)
max.names=c()
max.sharpe.ratio=0
max.w.opt=c()
for(i in 1:ncol(combinations)){
	if(i%%100==0){
		print(sprintf("Combination %d out of %d",i,ncol(combinations)))
	}
	names=names(instruments.sharp.ratios)[combinations[,i]]
	cov.matrix=var(cbind(all.r.daily[,names[1]],all.r.daily[,names[2]],all.r.daily[,names[3]],all.r.daily[,names[4]]))
	mu.vec=rbind(mean(all.r.daily[,names[1]]),mean(all.r.daily[,names[2]]),mean(all.r.daily[,names[3]]),mean(all.r.daily[,names[4]]))
	
	tryCatch({
		cov.matrix.inv=try(solve(cov.matrix),TRUE)
		if(!inherits(cov.matrix.inv,"try-error")){
			w.opt=cov.matrix.inv%*%mu.vec%*%solve(t(rep(1,instrument.count))%*%cov.matrix.inv%*%mu.vec)
			var.p=t(w.opt)%*%cov.matrix%*%w.opt
			mu.p=t(w.opt)%*%mu.vec
			sr=sqrt(TRADING_DAYS_IN_YEAR)*mu.p/sqrt(var.p)
			if(sr>max.sharpe.ratio){
				max.sharpe.ratio=sr
				max.w.opt=w.opt
				max.names=names
			}
		}
	},warning = function(w) {
		print(sprintf("warning: %s",w))
	}, error = function(e) {
		print(sprintf("error: %s",e))
		next
	})	
}

cov.matrix=cov(all.r.daily[,max.names])
sqrt(cov.matrix)
mu.vec=apply(all.r.daily[,max.names],2,mean)
mu.p=t(max.w.opt)%*%mu.vec
var.p=t(max.w.opt)%*%cov.matrix%*%max.w.opt
t(max.w.opt)%*%cov.matrix%*%max.w.opt
t(max.w.opt)%*%mu.vec
sqrt(TRADING_DAYS_IN_YEAR)*mu.p/sqrt(var.p)



