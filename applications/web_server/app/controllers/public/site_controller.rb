class Public::SiteController < ApplicationController
    
    respond_to :json, :html, :js
    layout :resolve_layout

    def index
        if user_signed_in?
					if params[:homepage] == nil
						redirect_to "/dashboard"
					else
						@resource = User.new
						respond_with(@resource)
					end
				else
					@resource = User.new
					respond_with(@resource)
				end
		end

		def getSwarmInfo
			@analytics = {}
			@analytics['swarm'] = nil
			@analytics['agents'] = []
			@analytics['city'] = nil
			@analytics['graffiti'] = []
			@analytics['swarm'] = Graphium::Swarm.where(:identifier => params[:swarm_identifier]).first
			if @analytics['swarm'] != nil

				@analytics['agents'] = Graphium::Agent.where(:swarm_identifier => @analytics['swarm'].identifier )
				@analytics['city'] = Graphium::City.find(@analytics['swarm'].city_id)

				if params[:classified_by_model] == "true"
					@analytics['graffiti'] = Graphium::Graffiti.where(:swarm_identifier => params[:swarm_identifier]).in(situation:  ['T','true_positive','false_positive'])
				else
					@analytics['graffiti'] = Graphium::Graffiti.where(:swarm_identifier => params[:swarm_identifier]).in(situation: ['false_negative','false_positive','true_positive'] )
				end

				@analytics['results'] = {}
				@analytics['results']['trues'] = Graphium::Pano.where(:swarm_identifier => params[:swarm_identifier] ).in(classification: ['T', 'TP', 'FP']).length
				@analytics['results']['falses'] = Graphium::Pano.where(:swarm_identifier => params[:swarm_identifier] ).in(classification: ['F', 'TN', 'FN']).length
				@analytics['results']['true_positive'] = Graphium::Pano.where(:classification => "TP", :swarm_identifier => params[:swarm_identifier] ).length
				@analytics['results']['true_negative'] = Graphium::Pano.where(:classification => "TN", :swarm_identifier => params[:swarm_identifier] ).length
				@analytics['results']['false_positive'] = Graphium::Pano.where(:classification => "FP", :swarm_identifier => params[:swarm_identifier] ).length
				@analytics['results']['false_negative'] = Graphium::Pano.where(:classification => "FN", :swarm_identifier => params[:swarm_identifier] ).length
				@analytics['results']['sensibility'] = (@analytics['results']['true_positive'].to_f / (@analytics['results']['true_positive']+@analytics['results']['false_positive']).to_f).round(4)
				@analytics['results']['especificility'] = (@analytics['results']['true_negative'].to_f / (@analytics['results']['false_negative']+@analytics['results']['true_negative']).to_f).round(4)
				@analytics['results']['preditive_positive'] = (@analytics['results']['false_positive'].to_f / (@analytics['results']['false_positive']+@analytics['results']['false_negative']).to_f).round(4)
				@analytics['results']['preditive_negative'] = (@analytics['results']['true_negative'].to_f / (@analytics['results']['false_positive']+@analytics['results']['true_negative']).to_f).round(4)
			end

			#@analytics_agent = Graphium::AgentStory.all
			respond_to do |format|
				format.json { render :json => @analytics }
			end
		end

		def getGraffitiInfo
			@information = {}
      @information['pano'] = nil
			@information['graffiti_date'] = ""
      @information['graffiti'] = Graphium::Graffiti.find(params[:id])
      if @information['graffiti'] != nil
        Graphium::Pano.where(pano_id: @information['graffiti'].pano_id).each do | pano |
          if pano.heading.to_i == @information['graffiti'].heading.to_i
              @information['pano'] = pano
          end
				end
				@information['graffiti_date'] = @information['graffiti'].id.generation_time.strftime('%d %b. %Y às %H:%M')
      end
			respond_to do |format|
				format.json { render :json => @information }
			end
		end

		def setRateToGraffiti

			graffiti = Graphium::Graffiti.find(params[:graffiti_id])
			logger.info 'INFO'
			logger.info graffiti
			logger.info 'IP'

			@information = {}
			logger.info request.env['REMOTE_ADDR']
			if not graffiti.nil?
				if ["no","yes","maybe"].include? params[:rate]
					if graffiti.rating.nil?
						graffiti.rating = {}
					end
					if graffiti.rating.key?(params[:rate])
						if graffiti.rating[params[:rate]].include? request.env['REMOTE_ADDR']
							@information['message'] = "IP "+request.env['REMOTE_ADDR']+" já computado."
						else
							graffiti.rating[params[:rate]].push request.env['REMOTE_ADDR']
							graffiti.save!
							@information['message'] = "Obrigado!"
						end
					else
						graffiti.rating[params[:rate]] = []
						graffiti.rating[params[:rate]].push request.env['REMOTE_ADDR']
						graffiti.save!
						@information['message'] = "Obrigado!"
					end
				else
					@information['message'] = "Rate não é válido"
				end
			else
				@information['message'] = "Graffiti não encontrado"
			end

			respond_to do |format|
				format.json { render :json => @information }
			end
		end

		def graffiti

		end

    def about

    end
    
    def version
        
		end

		def resolve_layout
			case action_name
			when "graffiti", "others"
				"graffiti"
			else
				"outside"
			end
		end
end
